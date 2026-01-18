import logging
import structlog
from pathlib import Path
from app.core.config import settings


def setup_logging() -> None:
    """
    Configure structured JSON logging for the application.
    """

    logging.basicConfig(
        level=settings.app_log_level,
        format="%(message)s",
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.app_log_level)
        ),
        cache_logger_on_first_use=True,
    )


def get_logger():
    """
    Returns a structured logger instance.
    """
    return structlog.get_logger()


def setup_audit_log_file() -> None:
    """
    Ensure audit log path exists.
    """
    if not settings.enable_audit_logs:
        return

    audit_path = Path(settings.audit_log_path)
    audit_path.parent.mkdir(parents=True, exist_ok=True)

    # Touch file so container has it ready
    audit_path.touch(exist_ok=True)
