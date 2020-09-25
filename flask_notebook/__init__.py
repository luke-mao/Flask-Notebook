from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import click


# create the app
app = Flask('flask_notebook')
app.config.from_pyfile('settings.py')

# create database and bootstrap
db = SQLAlchemy(app=app)
bootstrap = Bootstrap(app)


# this line must be placed at the bottom
# otherwise python will return "circular import" error
# since nothing is generated yet, so no "flask_notebook" project
from flask_notebook import views, errors,commands


# add a terminal command to initialize the database
# first drop all tables if existed, then create everything again
# type in terminal: "flask initdb"
@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database')
