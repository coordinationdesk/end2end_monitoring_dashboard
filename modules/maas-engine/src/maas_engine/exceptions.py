"""
Exception classes for maas-engine
"""


class MaasEngineException(Exception):
    """Base class for MAAS Engine exceptions"""


class MessageHandlerException(MaasEngineException):
    """Base class for exceptions in this module."""


class CannotProcessMessageException(MessageHandlerException):
    """Excpetion to use in the case a message cannot be process without recovery possible.
    For example to reject the message when this exception occurs

    Args:
        MessageHandlerException (MessageHandlerException): parent class
    """


class HandleMessageException(MessageHandlerException):
    """Excpetion to use in the case a message cannot be process but can be recover latter.
    For example to requeue the message when this exception occurs

    Args:
        MessageHandlerException (MessageHandlerException): parent class
    """
