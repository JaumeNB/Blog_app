### This is a blog application built with flask

# Main functionalities:

- Create blogposts with a rich editor (CKEditor) and uploading pictures/GIFs
- Save blogposts to DB with SQLAlchemy (SQLite or PostgreSQL engines)
- Edit blogposts
- Delete blogposts
- Search blogposts by keywords with ElasticSearch
- Admin page

# Usage:

- connect to a server by ssh (e.g. Ubuntu cloud server or Ubuntu Virtual Machine)
- install base dependencies(sudo apt-get -y install): python3, python3-venv, python3-dev, supervisor, nginx, git, sqlite
- clone this repository (git clone https://github.com/theselfengineer/blogapp)
- go to the blogapp folder (cd blogapp)
- create the virtual environment (python3 -m venv venv)
- log into the virtual environment created (source venv/bin/activate)
- install all the requirements (pip install -r requirements.txt)
- install gunicorn (pip install gunicorn)
- set environment variable to be registered every time login is made (echo "export FLASK_APP=blogapp.py" >> ~/.profile)
- set up gunicorn (web server to run privately) and supervisor (server monitoring) ==> generate file /etc/supervisor/conf.d/blogapp.conf
- set up nginx (web server to run publicly) ==> generate file /etc/nginx/sites-enabled/blogapp and add SSL certificate 
- reload supervisor service (sudo supervisorctl reload)
- reload nginx service (sudo service nginx reload)
- add an editor to the DB from the server to be able to login, create, edit and delete posts (flask shell, create editor and set password)
- connect to the IP address or domain name and enjoy!

# Deploying app updates

- go to virtual environment (source venv/bin/activate)
- download the version (git pull)
- stop the current server (sudo supervisorctl stop blogapp)
- upgrade the database (flask db upgrade)
- upgrade the translations (flask translate compile)
- start a new server (sudo supervisorctl start blogapp)


If you have any suggestion to improve the app or any doubt when trying to deploy it, don't hesitate to contact me.
