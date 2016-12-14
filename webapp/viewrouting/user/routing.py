 # -*- coding: utf-8 -*-
from flask import Blueprint,request,render_template,redirect,url_for,flash
from webapp.viewrouting.user.forms.login_form import LoginForm,ChangePasswordForm,RegistrationForm
from webapp.viewrouting.admin.forms.user_forms import CreateNewForm

from webapp.Models.user import User
from webapp.Models.db_basic import Session
from webapp.common import generate_md5
from flask_login import current_user,login_required
#import hashlib
from flask_login import login_user,logout_user,login_required

userRoute = Blueprint('userRoute', __name__,
                      template_folder='templates', static_folder='static')

##TODO customer views for login and registration https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login/app.py
@userRoute.route('/', methods=['GET', 'POST'])
def index():
    return render_template('user_temp/index.html')


@userRoute.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        email = login_form.email.data
        passwd_md5 = generate_md5(login_form.password.data) #hashlib.md5(login_form.password.data.encode('ascii'))
        password = passwd_md5

        s = Session()
        user = s.query(User).filter_by(email=email, password=password).first()  # User.query.filter_by(email=email,password=password).first()
        if user :
            login_user(user,remember = login_form.remember_me.data)
            next = request.args.get('next')
            # TODO
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            #if not next_is_valid(next):
            #    return abort(400)
            return redirect(next or url_for('homeRoute.index'))

        else:
            flash("User ID or Password invalid.",category='danger')

    return render_template('user_temp/login.html', form=login_form)


@userRoute.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('userRoute.login'))


@userRoute.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        email = login_form.email.data
        passwd_md5 = generate_md5(login_form.password.data) # hashlib.md5(login_form.password.data.encode('ascii'))
        password = passwd_md5

        s = Session()
        user = s.query(User).filter_by(email=email, password=password).first()  # User.query.filter_by(email=email,password=password).first()
        if user :
            login_user(user,remember = login_form.remember_me.data)
            next = request.args.get('next')
            # TODO
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            #if not next_is_valid(next):
            #    return abort(400)
            return redirect(next or url_for('homeRoute.index'))

        else:
            flash("User ID or Password invalid.",category='danger')

    return render_template('user_temp/admin_login.html', form=login_form)


@userRoute.route('/register', methods=['GET', 'POST'])
def register():
    register_user_form = RegistrationForm()
    if register_user_form.validate_on_submit():
        u = User()
        u.user_name = register_user_form.user_name.data
        u.email = register_user_form.email.data
        u.password = generate_md5(register_user_form.password.data)
        u.logo_link ='default_logo.png'
        u.valid_flg = 1
        u.is_admin = 0

        s = Session()
        s.add(u)
        s.commit()
        user = s.query(User).filter_by(email=u.email, password=u.password).first()  # User.query.filter_by(email=email,password=password).first()
        s.close()
        login_user(user)
        return redirect(url_for("homeRoute.index"))
    elif request.method == 'POST':
        flash(register_user_form.errors,category='danger')

    return render_template('user_temp/register.html', form=register_user_form)


@userRoute.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():
        email = current_user.email
        password_old = change_password_form.password_old.data
        password_new = change_password_form.password_new.data

        password_md5=generate_md5(password_old)
        session = Session()
        if session.query(User).filter_by(email=email,password=password_md5).first() is None:
            flash("Your old password is not right !",category='danger')
        else:
            password=generate_md5(password_new)
            s = Session()
            s.query(User).filter_by(email=email).update(
                {
                    "password": password
                }
             )
            s.commit()
            s.close()
            flash("Password changed successfully!",category='success')
    elif request.method == 'POST':
        flash(change_password_form.errors,category='danger')

    return render_template('user_temp/change_password.html', form=change_password_form)
