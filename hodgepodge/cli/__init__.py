from hodgepodge.cli.command_groups.files import files
from hodgepodge.cli.command_groups.file import file

import click


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


COMMAND_GROUPS = [
    file,
    files,
]
for command_group in COMMAND_GROUPS:
    cli.add_command(command_group)
