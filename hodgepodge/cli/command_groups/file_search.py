import os

from hodgepodge import click
from hodgepodge.toolkits.host.file.search import FileSearch
from hodgepodge.hashing import HASH_ALGORITHMS

import hodgepodge.click
import hodgepodge.types
import hodgepodge.ux
import click
import sys


@click.group(invoke_without_command=True)
@click.argument('roots', default=os.getcwd())
@click.option('--excluded-directories')
@click.option('--filename-glob-patterns')
@click.option('--min-file-size', type=int, default=None)
@click.option('--max-file-size', type=int, default=None)
@click.option('--max-depth', type=int, default=None)
@click.option('--max-results', type=int, default=None)
@click.option('--follow-symlinks/--no-symlinks', default=False)
@click.option('--follow-mounts/--no-mounts', default=True)
@click.pass_context
def file_search(ctx, roots: str, excluded_directories: str, filename_glob_patterns: str, min_file_size: int, max_file_size: int,
                max_depth: int, max_results: int, follow_symlinks: bool, follow_mounts: bool):
    """
    Search for one or more files.
    """
    ctx.obj['search'] = search = FileSearch(
        roots=hodgepodge.click.str_to_list(roots),
        excluded_directories=hodgepodge.click.str_to_list(excluded_directories),
        filename_glob_patterns=hodgepodge.click.str_to_list(filename_glob_patterns),
        min_file_size=min_file_size,
        max_file_size=max_file_size,
        max_depth=max_depth,
        max_results=max_results,
        follow_symlinks=follow_symlinks,
        follow_mounts=follow_mounts,
    )
    if not ctx.invoked_subcommand:
        for file in search:
            click.echo(file.path)


@file_search.command()
@click.pass_context
def count(ctx):
    """
    Count matching files.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    n = sum(1 for _ in search.iter_files(include_hashes=False))
    click.echo(n)


@file_search.command()
@click.option('--include-hashes/--no-hashes', help='({})'.format(','.join(HASH_ALGORITHMS)), default=False)
@click.pass_context
def get_metadata(ctx, include_hashes: bool):
    """
    Search for files.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    for file in search.iter_files(include_hashes=include_hashes):
        file = hodgepodge.types.dataclass_to_json(file)
        click.echo(file)


@file_search.command()
@click.pass_context
def get_paths(ctx):
    """
    Search for matching paths.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    for file in search:
        click.echo(file.path)


@file_search.command()
@click.pass_context
def get_total_size(ctx):
    """
    Combined size of selected files.
    """
    search = ctx.obj['search']
    assert isinstance(search, FileSearch)

    total = sum([f.size for f in search])
    click.echo(hodgepodge.ux.pretty_file_size(total))
