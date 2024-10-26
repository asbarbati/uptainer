"""Console script for virgo."""

import typer
import structlog
import logging
from pathlib import Path
from typing import Annotated
from .loader import Loader

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%d/%m/%Y %H:%M:%S", utc=False),
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)
log = structlog.get_logger()


def main(  # noqa D417
    config_file: Annotated[Path, typer.Option(help="Configuration file")] = "config.yml",
) -> None:
    """Main CLI function for Virgo project.

    Args:
        config (Path): Configuration file with PATH class.

    Returns:
        None
    """
    if not config_file.is_file():
        log.error("The config file seems not valid.")
        raise typer.Abort()
    loader = Loader(log=log, config_file=config_file)
    loader.run()


if __name__ == "__main__":
    typer.run(main)