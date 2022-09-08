import click
from rich.console import Console
from rich.theme import Theme
from rich import box

# Default configuration for Rich objects
tables = {
    'box': box.HORIZONTALS
}

# Theming for Rich
theme = Theme({
    'item_activated': 'green',
    'item_identification': 'blue'
})

# Create a reusable Rich-console
console = Console(theme=theme)


@click.group()
def cli():
    pass
