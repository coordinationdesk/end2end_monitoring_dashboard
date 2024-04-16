"""A thread class to run Flask application in background"""
import logging
import threading

from werkzeug.serving import make_server

LOGGER = logging.getLogger(__name__)

#
# FIXME use process instead of thread as healthcheck will be sometime too busy to answer
# quickly
#
class ServerThread(threading.Thread):
    """A thread to run Flask application in background"""

    def __init__(self, app, host, port, name="Flask application server"):
        threading.Thread.__init__(self, name=name)
        self.server = make_server(host, port, app)
        self.context = app.app_context()
        self.context.push()

    def run(self):
        """Override"""
        LOGGER.info("starting server %s:%d", *self.server.server_address)
        self.server.serve_forever()

    def shutdown(self):
        LOGGER.info("shutting down server %s:%d", *self.server.server_address)
        self.server.shutdown()
