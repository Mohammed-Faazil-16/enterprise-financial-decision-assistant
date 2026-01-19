import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

def get_logger(name: str = "efda"):
    return logging.getLogger(name)

# default logger
logger = get_logger()
