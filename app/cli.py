from app import app
import os
import click

"""
1. To extract all the texts to the .pot file, you can use the following command:
(venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .

2. The next step in the process is to create a translation for each language that will be supported in addition to the base one (create the .po file)
(venv) $ pybabel init -i messages.pot -d app/translations -l es creating catalog app/translations/es/LC_MESSAGES/messages.po based on messages.pot

2*. If .po file is already created, better update so all previous work is not lost:
(venv) $ pybabel update -i messages.pot -d app/translations

3. The messages.po file is a sort of source file for translations. When you want to start using these translated texts,
this file needs to be compiled into a format that is efficient to be used by the application at run-time:
(venv) $ pybabel compile -d app/translations compiling catalog app/translations/es/LC_MESSAGES/messages.po to app/translations/es/LC_MESSAGES/messages.mo
"""

@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass

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

@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

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
