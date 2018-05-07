from app import app, db, cli
from app.models import Blogpost, Editors, Messages, Logins

#to use flask shell command when using the python interpreter
#this way, all these modules are already imported
@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Blogpost': Blogpost,
            'Editors': Editors,
            'Messages': Messages,
            'Logins': Logins}
