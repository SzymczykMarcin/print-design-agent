"""Configure application logs and attach context to execution failures."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from time import perf_counter

from logo_vectorizer.errors import VectorizationError

LOGGER_NAME = "logo_vectorizer"
logger = logging.getLogger(LOGGER_NAME)


def configure_logging(*, debug: bool = False, log_file: Path | None = None) -> None:
    """Configure only application handlers; leave host and dependency logging intact."""
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file is not None:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)


@contextmanager
def execution_stage(name: str) -> Iterator[None]:
    """Time a stage and preserve its original failure as an exception cause."""
    started = perf_counter()
    logger.debug("Starting stage: %s", name)
    try:
        yield
    except Exception as exc:
        raise VectorizationError(f"{name} failed: {exc}") from exc
    else:
        logger.debug("Completed stage: %s (%.3fs)", name, perf_counter() - started)


def log_failure(message: str, *, debug: bool) -> None:
    """Log an active exception, including its traceback only in debug mode."""
    logger.error(message, exc_info=debug)
