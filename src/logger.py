"""
Controls the logging for the entire application.
"""
import os
import logging
import pathlib


logging.basicConfig(filename=pathlib.Path("logs", "BotLog.txt"),
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M.%S",
                    filemode="w")

logger = logging.getLogger()
logger.setLevel(int(os.getenv("LOG_LEVEL")))


def log_debug(thing: object) -> None:
    """ Logs at the debug level """
    logger.debug(thing)


def log_info(thing: object) -> None:
    """ Logs at the info level """
    print(thing)
    logger.info(thing)


def log_warn(thing: object) -> None:
    """ Logs at the warn level """
    print(thing)
    logger.warning(thing)


def log_critical(thing: object) -> None:
    """ Logs at the critical level """
    print(thing)
    logger.critical(thing)
