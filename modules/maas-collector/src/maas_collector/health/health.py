"""HealthCheck class"""

import dataclasses
import logging
import time
import typing

from opensearchpy.connection.connections import connections as es_connections
from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump


class ServiceHealthCheck:
    """Encapsulate healthcheck functions and a Flask application"""

    def __init__(self, consumer, tick_timeout=0) -> None:
        """
        Encapsulate flask application and health check status

        Args:
            consumer (_type_): _description_
            tick_timeout (int, optional): _description_. Defaults to 3600.
        """
        self.app = app = Flask(__name__)

        # Consumer class to monitor
        self.consumer = consumer

        self.tick_timeout = tick_timeout

        # last timestamp for later comparison
        self.last_tick = None

        self.health = HealthCheck()

        self.add_base_checks()

        # Add a flask route to expose information
        app.add_url_rule("/", "healthcheck", view_func=self.health.run)

        if logging.root.getEffectiveLevel() == logging.DEBUG:
            # prevent password dump in production
            self.envdump = EnvironmentDump()

            self.envdump.add_section("application", self.application_data)

            app.add_url_rule("/environment", "environment", view_func=self.envdump.run)

    def add_base_checks(self) -> None:
        """Default checks ( tick & database online check are added to the HealthCheck service)"""

        self.health.add_check(self.check_database)

        # add tick check
        self.health.add_check(self.check_tick)

    def add_check(self, check_func: typing.Callable) -> None:
        """Add a custom check function to the HealthCheck service"""
        self.health.add_check(check_func)

    def application_data(self):
        """add your own data to the environment dump"""
        status = {}

        # service statistics
        if hasattr(self.consumer, "stats"):
            status["statistics"] = dataclasses.asdict(self.consumer.stats)

        status["last_tick"] = self.last_tick

        return status

    def tick(self):
        """
        Store a timestamp
        """
        self.last_tick = time.time()

    def check_tick(self):
        """Check for loop timeout

        Returns:
            tuple: status (bool) and message
        """
        if not self.tick_timeout:
            return True, "OK: no ingestion loop timeout configured"

        if self.last_tick is None:
            return False, f"No tick() during loop (timeout={self.tick_timeout})"

        delta = time.time() - self.last_tick

        if delta >= self.tick_timeout:
            return (
                False,
                f"Ingestion loop stucked: delta {delta:.02f}s >=  {self.tick_timeout}s",
            )

        return True, f"No timeout, last delta: {delta:.02f}s <  {self.tick_timeout}s"

    def check_database(self):
        """
        ping database connection

        Returns:
            tuple: status (bool) and message
        """
        connection = es_connections.get_connection()

        if connection.ping():
            return True, "opensearch ping ok"

        return False, "Cannot ping opensearch"
