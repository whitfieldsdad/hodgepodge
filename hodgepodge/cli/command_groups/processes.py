import click

import hodgepodge.processes


@click.group()
def processes():
    """
    Query processes.
    """


@processes.command()
def get_processes():
    for process in hodgepodge.processes.iter_processes():
        click.echo(process.to_json())
