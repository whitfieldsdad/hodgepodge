from hodgepodge.cli.command_groups.file_search import file_search

import click


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


COMMAND_GROUPS = [
    file_search,
]
for command_group in COMMAND_GROUPS:
    cli.add_command(command_group)
