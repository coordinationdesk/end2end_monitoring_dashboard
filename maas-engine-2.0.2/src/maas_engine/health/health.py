"""HealthCheck class"""
import dataclasses

from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump


class ServiceHealthCheck:
    """Encapsulate healthcheck functions and a Flask application"""

    def __init__(self, consumer) -> None:

        self.app = app = Flask(__name__)

        # Consumer class to monitor
        self.consumer = consumer

        # helth checks callable
        self.health = HealthCheck()

        self.envdump = EnvironmentDump()

        # assign to py-healthcheck
        self.health.add_check(self.amqp_available)

        self.envdump.add_section("application", self.application_data)

        # Add a flask route to expose information
        app.add_url_rule("/", "healthcheck", view_func=self.health.run)

        app.add_url_rule("/environment", "environment", view_func=self.envdump.run)

    def amqp_available(self):
        """add check function to the healthcheck"""
        # TODO this only work for child implementation of MAASConsumer mixins
        message = "AMQP ok"
        if not self.consumer.is_ok:
            message = "AMQP not connected"
        return self.consumer.is_ok, message

    def application_data(self):
        """add your own data to the environment dump"""
        status = {}

        # amqp info
        info = self.consumer.amqp_connection.info()
        info["password"] = "***"
        status["amqp"] = info

        # service statistics
        if hasattr(self.consumer, "stats"):
            status["statistics"] = dataclasses.asdict(self.consumer.stats)

        return status
