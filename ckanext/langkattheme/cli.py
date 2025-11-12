import click


@click.group(short_help="langkattheme CLI.")
def langkattheme():
    """Langkat Theme Extension Command.
    """
    pass


@langkattheme.command()
@click.argument("name", default="langkattheme")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [langkattheme]
