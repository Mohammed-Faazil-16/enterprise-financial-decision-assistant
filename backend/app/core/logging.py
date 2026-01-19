import logging
import sys
from pathlib import Path

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"

_audit_logger = None


def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: str = "efda"):
    return logging.getLogger(name)


def setup_audit_log_file(log_dir: str = "logs", filename: str = "audit.log"):
    global _audit_logger

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / filename

    logger = logging.getLogger("audit")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(file_handler)

    _audit_logger = logger
    return logger


# DEFAULT LOGGER (for imports like `from app.core.logging import logger`)
setup_logging()
logger = get_logger()
