"""Mixins."""

from kombu.mixins import ConsumerMixin
from maas_engine.health import health
from maas_engine.health.serverthread import ServerThread


class MaasConsumerMixin(ConsumerMixin):
    """
    Mixin that adds healthcheck status about rabbitmq to consume loop in run()
    """

    # propagate abstract method so pylint is happy
    def get_consumers(self, Consumer, channel):
        raise NotImplementedError("Subclass responsibility")

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        self.is_ok = True

    def on_connection_error(self, exc, interval):
        self.is_ok = False
        super().on_connection_error(exc, interval)

    def on_connection_revived(self):
        self.is_ok = True

    def run(self, _tokens=1, **kwargs):
        # Init health check thread
        healthcheck = health.ServiceHealthCheck(self)

        heatlh_thread = ServerThread(
            healthcheck.app, self.args.healthcheck_hostname, self.args.healthcheck_port
        )

        heatlh_thread.start()
        try:
            super().run(_tokens, **kwargs)
        finally:
            heatlh_thread.shutdown()
            heatlh_thread.join()
