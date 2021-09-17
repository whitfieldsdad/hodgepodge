import click
import hodgepodge.types
import hodgepodge.files
import hodgepodge.ux
import logging

logger = logging.getLogger(__name__)


@click.group()
@click.argument('path', type=click.Path(exists=True))
@click.pass_context
def file(ctx: click.Context, path: str):
    """
    Learn more about a single file_search.
    """
    ctx.ensure_object(dict)
    ctx.obj['path'] = hodgepodge.files.get_real_path(path)


@file.command()
@click.pass_context
def get_metadata(ctx: click.Context):
    path = ctx.obj['path']
    try:
        info = hodgepodge.files.get_file_metadata(path)
    except FileNotFoundError as e:
        logger.error(e)
    else:
        data = hodgepodge.types.dataclass_to_json(info)
        click.echo(data)


@file.command()
@click.option('--easy-to-read/--hard-to-read', help="Display file sizes as strings rather than integers", default=True)
@click.pass_context
def get_size(ctx: click.Context, easy_to_read: bool):
    path = ctx.obj['path']
    try:
        size = hodgepodge.files.get_file_size(path)
    except FileNotFoundError as e:
        logger.error(e)
    else:
        if easy_to_read:
            size = hodgepodge.ux.pretty_file_size(size)
        click.echo(size)
