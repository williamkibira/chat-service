import datetime
import logging
import os
import platform
import sys
import threading
import structlog
from app.configuration import BuildInformation


class LogEntryProcessor:
    """
    Provide log entry processors as well as cached values that are expensive
    to create and thread local storage for request level variables.
    """
    # TODO: need some way to get a pod/node identifier instead of host - or perhaps that will work
    _HOST = platform.node().split('.')[0]
    _BI = BuildInformation.fetch()
    _TLS = threading.local()

    @staticmethod
    def get_request_id() -> str:
        if hasattr(LogEntryProcessor._TLS, "request_id"):
            return LogEntryProcessor._TLS.request_id
        return None

    @staticmethod
    def set_request_id(request_id: str) -> None:
        LogEntryProcessor._TLS.request_id = request_id

    @staticmethod
    def add_app_info(_, __, event_dict: dict) -> dict:
        """
        Add application level keys to the event dict
        """
        event_dict['logRepoName'] = LogEntryProcessor._BI.repository()
        event_dict['logServiceType'] = LogEntryProcessor._BI.environment()
        event_dict['logServiceName'] = LogEntryProcessor._BI.name()
        event_dict['logServiceVersion'] = LogEntryProcessor._BI.version()
        event_dict['logServiceInstance'] = LogEntryProcessor._HOST
        event_dict['logThreadId'] = threading.current_thread().getName()
        if LogEntryProcessor.get_request_id():
            # We are also used by the gunicorn logger so this may not be set
            event_dict['logRequestId'] = LogEntryProcessor.get_request_id()
        return event_dict

    @staticmethod
    def add_logger_name(logger, _, event_dict: dict) -> dict:
        """
        Add the logger name to the event dict - using loggerName consistent
        with existing platform logging.
        """
        # TODO: is this still needed - why do we need a loggerName if we include class
        record = event_dict.get("_record")
        if record is None:
            event_dict["loggerName"] = logger.name
        else:
            event_dict["loggerName"] = record.name
        return event_dict

    @staticmethod
    def add_timestamp(_, __, event_dict: dict) -> dict:
        """
        Add timestamp to the event dict - using an Analyitics appropriate time stamp
        CLC Analytics requires timestamps to be of form: YYYY-MM-DDTHH:MM:SS.sssZ
        python 3.5 strftime does not have millis; strftime is implemented on by the
        C library on the target OS - trying for something that is portable
        """
        now = datetime.datetime.utcnow()
        millis = '{:3d}'.format(int(now.microsecond / 1000))
        event_dict["timestamp"] = "%s.%sZ" % (now.strftime('%Y-%m-%dT%H:%M:%S'), millis)
        return event_dict

    @staticmethod
    def censor_password(_, __, event_dict: dict) -> dict:
        """
        Hide any passwords that appear in log entries
        """
        if event_dict.get('password'):
            event_dict['password'] = '*CENSORED*'
        return event_dict

    @staticmethod
    def cleanup_keynames(_, __, event_dict: dict) -> dict:
        """
        Final processing to ensure log record key names meet Analytics requirements
        """
        event_dict['logMessage'] = event_dict['event']
        del event_dict['event']
        return event_dict


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
    debug = os.environ.get('DEBUG', 'false') != 'false'
    logging.basicConfig(level='DEBUG' if debug else 'INFO',
                        stream=sys.stdout,
                        format="%(message)s")

    if os.getenv('LOG_MODE', 'JSON') == 'LOCAL':
        chain = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer()
        ]
    else:
        chain = [
            LogEntryProcessor.add_app_info,
            LogEntryProcessor.add_logger_name,
            LogEntryProcessor.add_timestamp,
            LogEntryProcessor.censor_password,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            LogEntryProcessor.cleanup_keynames,
            structlog.twisted.JSONRenderer()
        ]

    structlog.configure_once(
        processors=chain,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    structlog.configure_once(
        processors=chain,
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