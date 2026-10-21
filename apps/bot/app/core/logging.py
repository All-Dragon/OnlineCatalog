from logging.config import dictConfig
from socket import gethostname

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    }

    if settings.log_to_file:
        log_dir = settings.log_dir / gethostname()
        log_dir.mkdir(parents=True, exist_ok=True)

        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": str(log_dir / "app.log"),
            "maxBytes": settings.log_max_bytes,
            "backupCount": settings.log_max_files - 1,
            "encoding": "utf-8",
        }

    handler_names = list(handlers)

    loggers = {
        name: {
            "handlers": handler_names,
            "level": settings.log_level,
            "propagate": False,
        }
        for name in (
            "app",
            "aiogram",
            "uvicorn",
            "uvicorn.access",
            "uvicorn.error",
        )
    }

    for name in ("httpx", "httpcore"):
        loggers[name] = {
            "handlers": handler_names,
            "level": "WARNING",
            "propagate": False,
        }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": (
                        "%(asctime)s | %(levelname)-8s | %(name)s | "
                        "%(funcName)s | %(message)s"
                    ),
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
            },
            "handlers": handlers,
            "loggers": loggers,
            "root": {
                "handlers": handler_names,
                "level": "WARNING",
            },
        }
    )
