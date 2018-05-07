from app import app
import os
import click

"""-----------------CUSTOM FLASK COMMANDS-----------------"""

@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass

"""FLASK translate update"""
@translate.command()
def update():
    """Update all languages. Flow ==> flask translate update, (update translations in the .po file), flask translate compile"""
    #run commands and make sure that the return value is zero, which implies that the command did not return any error
    # command 1
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    #command 2*
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

"""FLASK translate compile"""
@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

"""FLASK translate init <LANG>"""
@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    #command 1
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    #command 2
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
