import click
from rich.console import Console
from rich.theme import Theme
from rich.logging import RichHandler
from rich import box
import logging

# Default configuration for Rich objects
tables = {
    'box': box.HORIZONTALS
}

# Theming for Rich
theme = Theme({
    'error': 'red',
    'error_highlight': 'yellow',
    'item_activated': 'green',
    'item_identification': 'blue'
})

# Create a reusable Rich-console
console = Console(theme=theme)


@click.group()
@click.option('-v', '--verbose', count=True)
def cli(verbose):
    # Set the default logging level
    default_level = logging.ERROR
    if verbose == 1:
        default_level = logging.WARNING
    elif verbose == 2:
        default_level = logging.INFO
    elif verbose > 2:
        default_level = logging.DEBUG

    # Configure logging
    logging.basicConfig(
        level=default_level,
        format='%(message)s',
        datefmt='[%X]',
        handlers=[RichHandler()])

    # Create a logger
    logger = logging.getLogger('cli')
    logger.debug('Started CLI and configured logging')
