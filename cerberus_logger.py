"""
Logging setup Module to make and look the code clean.

Usage:
    import cerberus_logger

    logger = cerberus_logger.setup_logging()
"""

import logging
import sys

def setup_logging(
        log_file = "cerberus.log",
        level = "INFO",
        silent_mode = False
):
    """
    Docstring for setup_logging
    
    Args:
        log_file: Name of the log file
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) ...niche mention karunga hi me
        silent_mode: if TRUE, dont show logs in the console, aur false me ye console/terminal pe logs dikhayega
    """

    level_map = {
        "DEBUG" : logging.DEBUG,
        "INFO" : logging.INFO,
        "WARNING" : logging.WARNING,
        "ERROR" : logging.ERROR,
        "CRITICAL" : logging.CRITICAL
    }
    log_level = level_map.get(level.upper(), logging.INFO)

    # Format dene ke liye ye Formatter hai
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H-%M-%S"
    )

    handlers = []

    # File handler (always log to file)
    file_handler = logging.FileHandler(
        log_file,
        mode="a", # Append mode
        encoding = "utf-8"
    )
    file_handler.setFormatter(formatter)
    handlers.append(file_handler)

    # Console handler
    if not silent_mode:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    # configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers
    )

    logger = logging.getLogger("cerberus")
    logger.info(f"Logging initialized. Level: {level}, File: {log_file}")

    return logger

def get_logger(name):
    return logging.getLogger(name)