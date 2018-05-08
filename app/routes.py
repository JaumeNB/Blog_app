from app import app, db, moment, ckeditor
from flask import render_template, request, redirect, url_for, session, flash, Markup, g, send_from_directory
from forms import PostForm, LoginForm
from datetime import datetime, date
from flask_login import login_user, logout_user, current_user, login_required
from collections import OrderedDict
from flask_babel import _, get_locale
from app.forms import LoginForm, PostForm
from app.models import Blogpost, Editors, Messages, Logins
import os

"""-----------------ROUTES-----------------"""

"""decorator executed before every view request"""
@app.before_request
def before_request():
    #returns the selected language and locale for a given request
    g.locale = str(get_locale())

"""INDEX"""
@app.route('/')
@app.route('/index')
def index():

    header = {
                "title" : "The Self Engineer",
                "subtitle" : _('A Blog for Makers'),
                "image_path" : "index-bg.jpg",
                "needed" : True
    }

    page = request.args.get('page', 1, type=int)

    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], True)

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None

    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', posts = posts.items, header = header, next_url=next_url, prev_url=prev_url)

"""POSTS"""
@app.route('/post/<int:post_id>')
def post(post_id):

    header = {
                "needed" : False
    }

    post = Blogpost.query.filter_by(id = post_id).one()

    return render_template('post.html', post = post, header = header)

"""ABOUT"""
@app.route('/about')
def about():

    header = {
                "title" : _('About Me'),
                "subtitle" : _('This is what I do.'),
                "image_path" : "about-bg.jpg",
                "needed" : True
    }

    return render_template('about.html', header = header)

"""CONTACT"""
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    header = {
                "title" : _('Contact me'),
                "subtitle" : _('We are just one click away!'),
                "image_path" : "contact-bg.jpg",
                "needed" : True
    }

    #if form is submited ==> post request
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        #write to DB
        message = Messages(name = name, email = email, message = message)
        db.session.add(message)
        db.session.commit()

        #redirect to index
        return redirect(url_for('index'))

    return render_template('contact.html', header = header)

"""LOG IN"""
@app.route('/login', methods=['GET', 'POST'])
def login():

    header = {
                "title" : 'Log in',
                "subtitle" : 'Manage your posts',
                "image_path" : "astronaut-bg.jpg",
                "needed" : True
    }

    #Imagine you have a user that is logged in, and the user
    #navigates to the /login URL of your application.
    #Clearly that is a mistake, so I want to not allow that.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    #if post request to edit form and is validated
    if form.validate_on_submit():

        #get form fields from the post request
        username = form.username.data
        password = form.password.data

        editor = Editors.query.filter_by(username=username).first()

        if editor is None or not editor.check_password(password):
            #password is not correct or user not found
            error = 'Invalid login'
            app.logger.info('Invalid login')
            return render_template('login.html', form = form, header = header, error = error)

        #user is logged in, session started
        login_user(editor, remember = True)

        #register to DB the login
        login = Logins(login = current_user)
        db.session.add(login)
        db.session.commit()

        #flash message
        flash('you are now logged in', 'success')

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)

    #load login template
    return render_template ('login.html', form = form, header = header)

"""LOGOUT"""
@app.route('/logout')
@login_required
def logout():

    logout_user()
    #flash message
    flash('You are now logged out', 'success')
    #redirect to log in
    return redirect(url_for('index'))

"""DASHBOARD"""
@app.route('/dashboard')
@login_required
def dashboard():


    header = {
                "title" : "Admin page",
                "subtitle" : "Manage your blog!",
                "image_path" : "manage-bg.jpg",
                "needed" : True,
                "dashboard_flash" : True
    }

    logins = Logins.query.order_by(Logins.timestamp.desc()).all()

    counter = {}

    for login in logins:

        parsed_date = datetime.strptime(str(login.timestamp),'%Y-%m-%d %H:%M:%S.%f')
        formated_date = parsed_date.strftime('%m/%d/%Y')

        if formated_date in counter:
            counter[formated_date] += 1
        else:
            counter[formated_date] = 1

    ordered_data = OrderedDict(sorted(counter.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%Y')))

    x_axis = list(ordered_data.keys())
    y_axis = list(ordered_data.values())


    return render_template('dashboard.html', header = header, logins = logins, values = y_axis, labels = x_axis)

"""MESSAGES"""
@app.route('/messages')
@login_required
def messages():

    header = {
                "title" : "Admin page",
                "subtitle" : "Manage your blog!",
                "image_path" : "manage-bg.jpg",
                "needed" : True,
                "dashboard_flash" : True
    }

    messages = Messages.query.order_by(Messages.date_posted.desc()).all()

    return render_template('messages.html', messages = messages, header = header)

"""ADD POST"""
@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():

    header = {
                "title" : "Admin page",
                "subtitle" : "Manage your blog!",
                "image_path" : "manage-bg.jpg",
                "needed" : True,
                "dashboard_flash" : True
    }

    editor = Editors.query.filter_by(id = current_user.id).one()

    form = PostForm()

    form.author.data = editor.name

    #app.logger.info(editor.name)

    #if post request to edit form and is validated
    if form.validate_on_submit():

        #get data from modified form
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        content = form.content.data

        #write to DB
        post = Blogpost(title = title, subtitle = subtitle, author = author, content = content, editor = editor)
        db.session.add(post)
        db.session.commit()

        #flash message
        flash('post published', 'success')

        #redirect to index
        return redirect(url_for('manage'))

    return render_template('add.html', form = form, header = header)

"""UPLOAD AN IMAGE TO THE SERVER"""
@app.route('/files/<filename>')
def files(filename):
	path = app.config['UPLOADED_PATH']
	return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
@ckeditor.uploader
def upload():
	f = request.files.get('upload')
	f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
	url = url_for('files', filename=f.filename)
	return url

"""MANAGE"""
@app.route('/manage', methods = ['GET', 'POST'])
@login_required
def manage():

    header = {
                "title" : "Admin page",
                "subtitle" : "Manage your blog!",
                "image_path" : "manage-bg.jpg",
                "needed" : True,
                "dashboard_flash" : True
    }

    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    #load template with articles
    return render_template('manage.html', posts = posts, header = header)

"""EDIT POST"""
@app.route('/edit_post/<string:id>', methods=['GET', 'POST'])
#check if it is logged in
@login_required
def edit_post(id):

    header = {
                "title" : "Admin page",
                "subtitle" : "Manage your blog!",
                "image_path" : "manage-bg.jpg",
                "needed" : True,
                "dashboard_flash" : True
    }

    post = Blogpost.query.filter_by(id = id).one()

    editor = Editors.query.filter_by(id = current_user.id).one()

    #get form
    form = PostForm(obj = post)

    #if post request to edit form and is validated
    if form.validate_on_submit():

        #get data from modified form
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        content = form.content.data

        #write to database
        post.title = title
        post.subtitle = subtitle
        post.author = author
        post.content = content
        post.editor_id = editor.id
        db.session.commit()

        #flash message, article has been updated
        flash('post updated', 'success')

        #redirect
        return redirect(url_for('manage'))

    #load template
    return render_template('edit_post.html', form = form, header = header)

"""DELETE_POST"""
@app.route('/delete_post/<string:id>', methods=['POST'])
@login_required
def delete_post(id):

    post_to_delete = Blogpost.query.filter_by(id = id).one()
    db.session.delete(post_to_delete)
    db.session.commit()

    #flash message
    flash('post deleted', 'success')

    #redirect to dashboard
    return redirect(url_for('manage'))
