import structlog


def initialize_logging() -> None:
    """
    Initialize our logging system:
    * the stdlib logging package for proper structlog use
    * structlog processor chain, etc.
    This should be called once for each application
    NOTES:
    * To enable human readable, colored, positional logging, set LOG_MODE=LOCAL
      Note that this hides many of the boilerplate log entry elements that is
      clutter for local development.
    """
    # debug =
    # logging.basicConfig(level='DEBUG' if debug else 'INFO',
    #                     stream=sys.stdout,
    #                     format="%(message)s")
    structlog.configure(
        processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.twisted.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.twisted.LoggerFactory(),
        wrapper_class=structlog.twisted.BoundLogger,
        cache_logger_on_first_use=True,
    )


class LoggerMixin:
    """
    A structured logger that is mixed in to each class
    The mixin methods follow structlog method signatures
    To record an exception in the log: exception type, message, and traceback::
        self._error("During shutdown, worker raised {} exception: {}".format(
                    type(exc).__name__, exc), exc_info=exc)
    """

    @property
    def _logger(self):
        if not getattr(self, '__logger__', None):
            self.__logger__ = structlog.get_logger(type(self).__name__)
        return self.__logger__

    def _debug(self, msg, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, level="Debug", **kwargs)

    def _error(self, msg, *args, **kwargs) -> None:
        self._logger.error(msg, *args, level="Error", **kwargs)

    def _info(self, msg, *args, **kwargs) -> None:
        self._logger.info(msg, *args, level="Info", **kwargs)

    def _warning(self, msg, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, level="Warn", **kwargs)


class Logger(LoggerMixin):
    """
    An instantiable class allowing non-protected access to the LoggerMixin methods.
    Intended for use with functions (things without classes).
    When using this class, you must supply a logger name; by convention, the dotted
    package path.
    """

    def __init__(self, name):
        """
        :param name: required logger name - use dotted package path
        """
        if name is not None and not getattr(self, '__logger__', None):
            self.__logger__ = structlog.get_logger(name)

    def debug(self, msg, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)
