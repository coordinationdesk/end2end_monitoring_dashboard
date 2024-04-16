import datetime
from functools import wraps


def duration_inspector(func):
    """A decorator to know duration of a function

    Args:
        func (function): the func wrapped
    """

    @wraps(func)
    def wrapper(*args, **kwds):
        class_instance = args[0]
        class_instance.logger.debug("[%s] - Start", func.__name__.upper())
        start = datetime.datetime.now()
        function_return = func(*args, **kwds)
        end = datetime.datetime.now()
        duration = end - start
        class_instance.logger.info(
            "[%s][STATS] - Duration: %s", func.__name__.upper(), duration
        )
        class_instance.logger.debug("[%s] - End", func.__name__.upper())

        return function_return

    return wrapper
