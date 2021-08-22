import click

from app.core.configuration import Configuration
from app.core.database.migrations import SQLMigrationHandler
from app.settings import MIGRATIONS_FOLDER


@click.command(help='run sql migrations on database')
def migrate() -> None:
    configuration: Configuration = Configuration.get_instance()

    click.echo("DATABASE URL: {}\n".format(configuration.database_uri()))
    click.echo("MIGRATIONS FOLDER: {}\n".format(MIGRATIONS_FOLDER))

    handler = SQLMigrationHandler(
        database_url=configuration.database_uri(),
        migration_folder=MIGRATIONS_FOLDER
    )
    handler.migrate()


@click.command(help='rollback sql migrations on database')
def rollback() -> None:
    configuration: Configuration = Configuration.get_instance()

    click.echo("DATABASE URL: {}\n".format(configuration.database_uri()))
    click.echo("MIGRATIONS FOLDER: {}\n".format(MIGRATIONS_FOLDER))

    handler = SQLMigrationHandler(
        database_url=configuration.database_uri(),
        migration_folder=MIGRATIONS_FOLDER
    )
    handler.rollback()


@click.group()
def cli() -> None:
    pass


cli.add_command(rollback)
cli.add_command(migrate)

if __name__ == "__main__":
    cli()
