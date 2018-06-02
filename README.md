### This is a blog application built with flask

# Main functionalities:

- Create blogposts with a rich editor (CKEditor) and upload pictures/GIFs on local drive
- Save blogposts to DB with SQLAlchemy (SQLite, MySQL or PostgreSQL engines)
- Edit blogposts
- Delete blogposts
- Admin page

# Usage:

- connect to a server by ssh (e.g. Ubuntu cloud server or Ubuntu Virtual Machine)
- install base dependencies(sudo apt-get -y install): python3, python3-venv, python3-dev, supervisor, nginx, git, sqlite, ufw
- clone this repository (git clone https://github.com/theselfengineer/blogapp)
- go to the blogapp folder (cd blogapp)
- create the virtual environment (python3 -m venv venv)
- log into the virtual environment created (source venv/bin/activate)
- install wheel (pip install wheel)
- install all the requirements (pip install -r requirements.txt)
- install gunicorn (pip install gunicorn)
- set environment variable to be registered every time login is made (echo "export FLASK_APP=blogapp.py" >> ~/.profile)
- set up gunicorn (web server to run privately) and supervisor (server monitoring) ==> generate file /etc/supervisor/conf.d/blogapp.conf
- set up nginx (web server to run publicly) ==> generate file /etc/nginx/sites-enabled/blogapp and add SSL certificate
- set up firewall(sudo ufw allow ssh, sudo ufw allow http, sudo ufw allow 443/tcp, sudo ufw --force enable)
- reload supervisor service (sudo supervisorctl reload)
- reload nginx service (sudo service nginx reload)
- create the DB (blog.db in /DB)
- Access virtual environment  to create the tables with migrate (flask shell, flask db migrate, flask db upgrade)
- add an editor to the DB from the server to be able to login, create, edit and delete posts:

    - flask shell
    - editor = Editors(name = 'name', username = 'username')
    - db.session.add(editor)
    - db.session.commit()
    - editor.set_password('password')
    - db.session.commit()

- connect to the IP address or domain name and enjoy!

If you have any doubt, please refer to this excellent post:

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux

# Deploying app updates

- go to virtual environment (source venv/bin/activate)
- download the version (git pull)
- stop the current server (sudo supervisorctl stop blogapp)
- upgrade the database (flask db upgrade)
- upgrade the translations (flask translate compile)
- start a new server (sudo supervisorctl start blogapp)

# Future improvements

- Add article tags
- Add post search by tags
- Add post search by content
- Add multilingual support for posts



If you have any suggestion to improve the app or any doubt when trying to deploy it, don't hesitate to contact me.
