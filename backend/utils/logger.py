import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)

    # Create handlers if they don't exist
    if not logger.handlers:
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # File handler for errors
        file_handler = RotatingFileHandler(
            "logs/errors.log", maxBytes=10485760, backupCount=5  # 10MB
        )
        console_handler = logging.StreamHandler()

        # Create formatters and add it to handlers
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
