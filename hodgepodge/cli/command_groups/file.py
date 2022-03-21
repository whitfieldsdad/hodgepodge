from hodgepodge import click
from hodgepodge.files import FOLLOW_SYMLINKS_BY_DEFAULT

import hodgepodge.files
import hodgepodge.click
import hodgepodge.types
import hodgepodge.ux
import logging
import click

logger = logging.getLogger(__name__)


@click.group()
def file():
    """
    Work with individual files.
    """
    pass


@file.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--include-file-hashes/--exclude-file-hashes', default=True)
def get_metadata(path: str, include_file_hashes: bool):
    try:
        info = hodgepodge.files.get_metadata(path, include_file_hashes=include_file_hashes)
    except FileNotFoundError as e:
        logger.error(e)
    else:
        data = hodgepodge.types.dataclass_to_json(info)
        click.echo(data)


@file.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--easy-to-read/--hard-to-read', help="Display file sizes as strings rather than integers", default=True)
def get_size(path: str, easy_to_read: bool):
    try:
        size = hodgepodge.files.get_size(path)
    except FileNotFoundError as e:
        logger.error(e)
    else:
        if easy_to_read:
            size = hodgepodge.ux.get_pretty_byte_count(size)
        click.echo(size)
