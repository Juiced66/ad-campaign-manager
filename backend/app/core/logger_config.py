import json
import logging
import logging.config
import os


def setup_logging():
    """Configures application-wide logging."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
            "json": {
                "format": json.dumps(
                    {
                        "timestamp": "%(asctime)s",
                        "level": "%(levelname)s",
                        "logger": "%(name)s",
                        "message": "%(message)s",
                    }
                )
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": os.getenv("LOG_LEVEL", "DEBUG"),
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "json",
                "filename": "app.log",
                "when": "midnight",
                "backupCount": 7,
                "level": os.getenv("LOG_LEVEL", "INFO"),
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": os.getenv("LOG_LEVEL", "DEBUG"),
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(logging_config)
