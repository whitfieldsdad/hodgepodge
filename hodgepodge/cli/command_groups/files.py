from hodgepodge import click
from hodgepodge.constants import INCLUDE_FILE_HASHES_BY_DEFAULT, FOLLOW_MOUNT_POINTS_BY_DEFAULT, \
    FOLLOW_SYMLINKS_BY_DEFAULT, STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT
from hodgepodge.toolkits.host.file_search.file_search import FileSearch
from hodgepodge.hashing import HASH_ALGORITHMS

import hodgepodge.click
import hodgepodge.types
import hodgepodge.ux
import click
import os


@click.group(invoke_without_command=True)
@click.argument('roots', default=os.getcwd())
@click.option('--ignored-paths')
@click.option('--filename-patterns')
@click.option('--case-sensitive/--case-insensitive', default=STRING_COMPARISON_IS_CASE_SENSITIVE_BY_DEFAULT)
@click.option('--min-file-size', type=int, default=None)
@click.option('--max-file-size', type=int, default=None)
@click.option('--max-search-depth', type=int, default=None)
@click.option('--max-search-results', type=int, default=None)
@click.option('--follow-symlinks/--ignore-symlinks', default=FOLLOW_SYMLINKS_BY_DEFAULT)
@click.option('--follow-mount-points/--ignore-mount-points', default=FOLLOW_MOUNT_POINTS_BY_DEFAULT)
@click.option('--include-file-hashes/--no-file-hashes', help='({})'.format(','.join(HASH_ALGORITHMS)), default=INCLUDE_FILE_HASHES_BY_DEFAULT)
@click.pass_context
def files(ctx, roots: str, ignored_paths: str, filename_patterns: str, case_sensitive: bool, min_file_size: int,
          max_file_size: int, max_search_depth: int, max_search_results: int, follow_symlinks: bool,
          follow_mount_points: bool, include_file_hashes: bool):
    """
    Search for one or more files.
    """
    roots = hodgepodge.click.str_to_list(roots)
    ignored_paths = hodgepodge.click.str_to_list(ignored_paths)
    filename_patterns = hodgepodge.click.str_to_list(filename_patterns)

    ctx.obj['search'] = search = FileSearch(
        roots=roots,
        ignored_paths=ignored_paths,
        filename_patterns=filename_patterns,
        case_sensitive=case_sensitive,
        min_file_size=min_file_size,
        max_file_size=max_file_size,
        max_search_depth=max_search_depth,
        max_search_results=max_search_results,
        follow_symlinks=follow_symlinks,
        follow_mount_points=follow_mount_points,
        include_file_hashes=include_file_hashes,
    )
    if not ctx.invoked_subcommand:
        for file in search:
            click.echo(file.path)


@files.command()
@click.pass_context
def count(ctx):
    """
    Count matching files.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    n = sum(1 for _ in search)
    click.echo(n)


@files.command()
@click.pass_context
def get_metadata(ctx):
    """
    Search for files.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    for file in search:
        file = hodgepodge.types.dataclass_to_json(file)
        click.echo(file)


@files.command()
@click.pass_context
def get_paths(ctx):
    """
    Search for matching paths.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    for file in search:
        click.echo(file.path)


@files.command()
@click.option('--easy-to-read/--hard-to-read', default=True)
@click.pass_context
def get_total_size(ctx, easy_to_read: bool):
    """
    Combined size of selected files.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    sz = sum(f.size for f in search)
    if easy_to_read:
        sz = hodgepodge.ux.pretty_file_size(sz)
    click.echo(sz)
