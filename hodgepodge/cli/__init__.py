from hodgepodge.cli.command_groups.file import file
from hodgepodge.cli.command_groups.commands import commands
from hodgepodge.cli.command_groups.processes import processes

import click


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


COMMAND_GROUPS = [
    file,
    commands,
    processes,
]
for command_group in COMMAND_GROUPS:
    cli.add_command(command_group)
