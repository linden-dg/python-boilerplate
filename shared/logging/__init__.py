import logging
from colorama import init, Fore, Style
from shared.config import config

init(autoreset=True)
SUCCESS_LOG_LEVEL = 25


class _ColorFormatter(logging.Formatter):
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "DEBUG": Fore.WHITE,
        "INFO": Fore.BLUE,
        "WARNING": Fore.YELLOW,
        "SUCCESS": Fore.GREEN,
        "ERROR": Fore.MAGENTA,
        "CRITICAL": Style.BRIGHT + Fore.RED,
    }

    ICONS = {
        "DEBUG": "🔍",
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "SUCCESS": "✅",
        "ERROR": "❌",
        # "CRITICAL": "⛔"
        "CRITICAL": "🔥",
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        icon = self.ICONS.get(record.levelname, "")
        if color:
            record.name = color + record.name + Fore.WHITE
            record.icon = (
                color + record.icon if hasattr(record, "icon") else icon + Fore.WHITE
            )
            # record.name = Fore.WHITE + record.name + Fore.WHITE
            record.levelname = color + record.levelname + Fore.WHITE
            record.msg = color + record.msg + Fore.WHITE
        return logging.Formatter.format(self, record)


class _ColorLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name)
        # color_formatter = _ColorFormatter("%(levelname)-18s :: %(name)-10s :: %(message)s")
        color_formatter = _ColorFormatter("%(icon)s %(name)-10s :: %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS_LOG_LEVEL):
            self._log(SUCCESS_LOG_LEVEL, msg, args, **kwargs)


# %%
# logging.basicConfig(level=Config.log_level)
logging.addLevelName(SUCCESS_LOG_LEVEL, "SUCCESS")
logging.setLoggerClass(_ColorLogger)

Logger = logging


def getLogger(name: str, level=config.log_level):
    _logger = Logger.getLogger(name)
    _logger.setLevel(level)
    return _logger


# %% testing logging
#
# logger = logging.getLogger(__name__)
# logger.setLevel(Logger.DEBUG)
# logger.debug("This is a debug message", extra={"icon": "🔑"})
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.success("This is a success message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
