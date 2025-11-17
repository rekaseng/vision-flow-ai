import logging
from logging.handlers import TimedRotatingFileHandler
import os
from src.config.settings import settings

def setup_logger():
    log_dir = settings.logging.log_dir
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(module)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Rotating File Handler
    file_path = os.path.join(log_dir, settings.logging.log_file)
    file_handler = TimedRotatingFileHandler(
        file_path, when="midnight", interval=1, backupCount=settings.logging.retention_days
    )
    file_handler.setFormatter(formatter)

    logger = logging.getLogger("visionflow")
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
