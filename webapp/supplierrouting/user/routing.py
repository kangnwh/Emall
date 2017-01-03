 # -*- coding: utf-8 -*-
from flask import Blueprint,request,render_template,redirect,url_for,flash,render_template_string,abort
from webapp.supplierrouting.user.forms.login_form import LoginForm,ChangePasswordForm,RegistrationForm

# from webapp.Models.user import User
from flask_paginate import Pagination
from flask_sqlalchemy import BaseQuery
from webapp.Models.supplier import Supplier
from webapp.Models.db_basic import Session
from webapp.Models import get_pending_order_count,get_pending_quote_count,get_supplier_level
from webapp.common import generate_md5
from flask_login import current_user,login_user,logout_user,login_required
from webapp.supplierrouting.order.forms.order_forms import UpdateQuoteForm
#models
from webapp.Models.order_system import Order_system
from webapp.Models.quote_system import Quote_system
#CONFIG
import webapp.config.customer_config as customer_config


userRoute = Blueprint('userRoute', __name__,
                      template_folder='templates', static_folder='static')

@userRoute.route('/', methods=['GET', 'POST'])
def index():
    return render_template('admin_temp/index.html')


@userRoute.route('/login', methods=[ 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        email = login_form.email.data
        passwd_md5 = generate_md5(login_form.password.data) #hashlib.md5(login_form.password.data.encode('ascii'))
        password = passwd_md5
        s = Session()
        user = s.query(Supplier).filter_by(email=email, password=password).first()  # User.query.filter_by(email=email,password=password).first()
        if user :
            login_user(user,remember = login_form.remember_me.data)
            next = request.args.get('next')
            # TODO
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            #if not next_is_valid(next):
            #    return abort(400)
            #return redirect(next or url_for('userRoute.index'))
            flash("User {user_name} login successfully.".format(user_name=user.supplier_name),'success')
            next = login_form.next.data
            return redirect(next)

        else:
            flash("User ID or Password invalid.",category='danger')

    return redirect(url_for("userRoute.register_login"))


@userRoute.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('supplierRoute.index'))

@userRoute.route('/register', methods=['POST'])
def register():
    register_user_form = RegistrationForm()
    if register_user_form.validate_on_submit():
        supplier = Supplier()
        supplier.supplier_name = register_user_form.supplier_name.data
        supplier.email = register_user_form.email.data
        supplier.password = generate_md5(register_user_form.password.data)
        supplier.address =register_user_form.address.data
        supplier.tel=register_user_form.tel.data
        supplier.valid_flg = 1
        supplier.supplier_points = 0

        s = Session()
        s.add(supplier)
        s.commit()
        user = s.query(Supplier).filter_by(email=supplier.email, password=supplier.password).first()  # User.query.filter_by(email=email,password=password).first()
        s.close()
        login_user(user)
        flash("User {user_name} registerd successfully.".format(user_name=supplier.supplier_name),'success')
        next = register_user_form.next.data
        return redirect(next)
    elif request.method == 'POST':
        flash(register_user_form.errors,category='danger')

    return redirect(url_for("userRoute.register_login"))

@userRoute.route('/register_login', methods=['GET'])
def register_login():
    next = request.args.get("next","")
    register_user_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('user_temp/register_or_login.html',
                           loginForm=login_form,
                           registerForm=register_user_form,
                           next=next)


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
        if session.query(Supplier).filter_by(email=email,password=password_md5).first() is None:
            flash("Your old password is not right !",category='danger')
        else:
            password=generate_md5(password_new)
            s = Session()
            s.query(Supplier).filter_by(email=email).update(
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

@userRoute.route("/user_orders/<type>",methods=["GET"])
@login_required
def user_orders(type):
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)

    s = Session()
    order_list_base = BaseQuery(Order_system,s).filter_by(supplier_id=current_user.supplier_id)
    s.close()
    if type == 'finished':
        order_list = order_list_base.filter_by(order_stat=5).order_by(Order_system.order_create_dt.desc()).paginate(page,customer_config.USER_ORDER_PER_PAGE, False) #BaseQuery(Order_system,s).filter_by(order_stat=5).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)
        #s.query(Order_system).filter_by(order_stat=5)
    elif type=='ongoing':
        order_list = order_list_base.filter(Order_system.order_stat.in_([1,2,3,4])).order_by(Order_system.order_create_dt.desc()).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)# BaseQuery(Order_system,s).filter(Order_system.order_stat.in_(1,2,3,4)).paginate(page,customer_config.USER_ORDER_PER_PAGE, False) #s.query(Order_system).filter(Order_system.order_stat.in_(1,2,3,4))
    elif type=='canceled':
        order_list = order_list_base.filter(Order_system.order_stat.in_([6,7])).order_by(Order_system.order_create_dt.desc()).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)#BaseQuery(Order_system,s).filter(Order_system.order_stat.in_(6,7)).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)#s.query(Order_system).filter(Order_system.order_stat.in_(6,7))
    else:
        abort(404)
    pagination = Pagination(page=page, total=order_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Order List',
                            per_page=customer_config.USER_ORDER_PER_PAGE)
    return render_template('user_temp/my_orders.html',order_active=type,
                           order_list=order_list,
                           pagination=pagination)

@userRoute.route("/user_quotes/<type>",methods=["GET"])
@login_required
def user_quotes(type):
    supp_update_quote_form = UpdateQuoteForm()
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)

    s = Session()
    quote_list_base = BaseQuery(Quote_system,s).filter_by(supplier_id=current_user.supplier_id)

    if type == 'finished':
        quote_list = quote_list_base.filter(Quote_system.is_return_flg == 1).order_by(Quote_system.quote_create_time.desc()).paginate(page,customer_config.USER_QUOTE_PER_PAGE, False)
    elif type=='ongoing':
        quote_list = quote_list_base.filter(Quote_system.is_return_flg == 0).order_by(Quote_system.quote_create_time.desc()).paginate(page,customer_config.USER_QUOTE_PER_PAGE, False)
    else:
        abort(404)

    pagination = Pagination(page=page, total=quote_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Quote List',
                            per_page=customer_config.USER_QUOTE_PER_PAGE)

    return render_template('user_temp/my_quotes.html',quote_active=type,
                           quote_list=quote_list,
                           supp_update_quote_form=supp_update_quote_form,
                           pagination=pagination)