import click

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///samizdat.db', echo=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base()
Base.query = session.query_property()


def init_app(app):
    app.cli.add_command(init_db)


@click.command('init-db')
def init_db():
    Base.metadata.create_all(bind=engine)
    click.echo('Inited the db.')
