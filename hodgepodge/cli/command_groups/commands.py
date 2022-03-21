import hodgepodge.commands
import hodgepodge.processes
import hodgepodge.types
import click


@click.group()
def commands():
    """
    Execute commands.
    """


@commands.command('exec')
@click.argument('command')
def execute_command(command: str):
    process = hodgepodge.commands.execute_command(command)
    txt = hodgepodge.types.dataclass_to_json(process)
    click.echo(txt)
