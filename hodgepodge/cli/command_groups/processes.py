from hodgepodge.click import str_to_ints, str_to_strs

import click
import hodgepodge.processes


@click.group()
def processes():
    """
    Query processes.
    """


@processes.command()
@click.option('--pids')
@click.option('--ppids')
@click.option('--names')
@click.option('--hide-empty-values/--show-empty-values', 'remove_empty_values')
def get_processes(pids: str, ppids: str, names: str, remove_empty_values: bool):
    for process in hodgepodge.processes.iter_processes(
        pids=str_to_ints(pids),
        ppids=str_to_ints(ppids),
        names=str_to_strs(names),
    ):
        click.echo(process.to_json(remove_empty_values=remove_empty_values))
