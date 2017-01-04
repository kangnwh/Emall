 # -*- coding: utf-8 -*-
from flask import Blueprint,request,render_template,redirect,url_for,flash,render_template_string,jsonify,abort
from webapp.viewrouting.user.forms.login_form import LoginForm,ChangePasswordForm,RegistrationForm
from webapp.viewrouting.admin.forms.user_forms import CreateNewForm
from flask_paginate import Pagination
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc,null,or_
from webapp.Models.user import User
from webapp.Models.db_basic import Session
from webapp.Models.order_system import Order_system
from webapp.Models.quote_system import Quote_system
from webapp.common import generate_md5,order_search_filter,quote_search_filter
from flask_login import current_user,login_user,logout_user,login_required
#CONFIG
import webapp.config.customer_config as customer_config

userRoute = Blueprint('userRoute', __name__,
                      template_folder='templates', static_folder='static')

##TODO customer views for login and registration https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login/app.py
@userRoute.route('/', methods=['GET', 'POST'])
@login_required
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
            next = login_form.next.data
            # TODO
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            #if not next_is_valid(next):
            #    return abort(400)
            #return redirect(next or url_for('userRoute.index'))
            flash("User {user_name} login successfully.".format(user_name=user.user_name),'success')
            return redirect(next) if next else render_template("reload_parent.html")

        else:
            flash("User ID or Password invalid.",category='danger')

    return redirect(url_for("userRoute.register_login"))


@userRoute.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('homeRoute.index'))

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
        u.is_paid = 0
        u.credit_points = 0
        u.is_subscribe = register_user_form.is_subscribe.data

        s = Session()
        s.add(u)
        s.commit()
        user = s.query(User).filter_by(email=u.email, password=u.password).first()  # User.query.filter_by(email=email,password=password).first()
        s.close()
        login_user(user)
        next = register_user_form.next.data
        flash("User {user_name} registerd successfully.".format(user_name=u.user_name),'success')
        return redirect(next) if next else render_template("reload_parent.html")
    elif request.method == 'POST':
        flash(register_user_form.errors,category='danger')

    return redirect(url_for("userRoute.register_login"))

@userRoute.route('/register_login', methods=['GET'])
def register_login():
    next = request.args.get('next','')
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

@userRoute.route('/user_management', methods=['GET', 'POST'])
@login_required
def user_management():
    user_id=current_user.user_id
    s = Session()
    user_list = s.query(User).filter_by(user_id=user_id).first()
    s.close
    return render_template('user_temp/user_management.html',
                           user_list=user_list)

@userRoute.route('/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    user_id = current_user.user_id
    is_subscribe=request.form.get('is_subscribe')
    if is_subscribe:
        s = Session()
        s.query(User).filter_by(user_id=user_id).update(
                {
                    "is_subscribe": is_subscribe
                }
        )
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for update user',category='danger')
        return jsonify(result='failed')
@userRoute.route("/user_orders/<type>",methods=["GET"])
@login_required
def user_orders(type):
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)

    s = Session()
    order_list_base = BaseQuery(Order_system,s).filter_by(user_id=current_user.user_id)
    if type == 'finished':
        order_list = order_list_base.filter_by(order_stat=5).order_by(Order_system.order_create_dt.desc()).paginate(page,customer_config.USER_ORDER_PER_PAGE, False) #BaseQuery(Order_system,s).filter_by(order_stat=5).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)
        #s.query(Order_system).filter_by(order_stat=5)
    elif type=='ongoing':
        order_list = order_list_base.filter(Order_system.order_stat.in_([1,2,3,4])).order_by(Order_system.order_create_dt.desc()).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)# BaseQuery(Order_system,s).filter(Order_system.order_stat.in_(1,2,3,4)).paginate(page,customer_config.USER_ORDER_PER_PAGE, False) #s.query(Order_system).filter(Order_system.order_stat.in_(1,2,3,4))
    elif type=='canceled':
        order_list = order_list_base.filter(Order_system.order_stat.in_([6,7,8])).order_by(Order_system.order_create_dt.desc()).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)#BaseQuery(Order_system,s).filter(Order_system.order_stat.in_(6,7)).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)#s.query(Order_system).filter(Order_system.order_stat.in_(6,7))
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
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)

    s = Session()
    quote_list_base = BaseQuery(Quote_system,s).filter_by(user_id=current_user.user_id)

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
                           pagination=pagination)

@userRoute.route("order_search",methods=["GET"])
@login_required
def order_search():
    key_words = request.args.get("q")
    if key_words:
        search_words = key_words.split(" ")
        like_words = ['%{w}%'.format(w=w) for w in search_words]

        page = request.args.get('page', type=int, default=1)

        s = Session()
        # sub_cat_id = sub_cat_id if sub_cat_id>0 else s.query(func.min(Prod_sub_cat.prod_cat_id).label('min')).first().min
        # prod_cat_sub = s.query(Prod_sub_cat).filter_by(prod_cat_sub_id=sub_cat_id).first()
        query_base = BaseQuery(Order_system,s).filter(Order_system.user_id == current_user.user_id)

        # order_list = query_base.filter(or_(*([Order_system.prod_name.like(w) for w in like_words]+
        #                                       [Order_system.imprint_info.like(w) for w in like_words]+
        #                                       [Order_system.colors.like(w) for w in like_words]+
        #                                       [Order_system.user_comments.like(w) for w in like_words]+
        #                                       [Order_system.supplier_comments.like(w) for w in like_words]
        #                                      +[Order_system.client_order_id.like(w) for w in like_words]
        #                                     ))).paginate(page,customer_config.USER_ORDER_PER_PAGE, False)
        #
        # pagination = Pagination(page=page, total=order_list.total,
        #                         search=None, css_framework='bootstrap3',
        #                         record_name='Prod Information',
        #                         per_page=customer_config.PROD_NUM_PER_PAGE)
        order_list,pagination = order_search_filter(key_words,query_base,page)
        return render_template('user_temp/my_orders.html',
                               key_words = key_words,
                               type = 'search',
                               # supplier_list = supplier_list,
                               # active_supplier = supplier_id,
                               order_list=order_list,
                               pagination=pagination)
    else:
        flash("Please provide key words when you search something","warning")
        return redirect(url_for("userRoute.user_orders",type="ongoing"))

@userRoute.route("/quote_search",methods=["GET"])
@login_required
def quote_search():
    key_words = request.args.get("q")
    if key_words:
        # search_words = key_words.split(" ")
        # like_words = ['%{w}%'.format(w=w) for w in search_words]

        page = request.args.get('page', type=int, default=1)

        s = Session()
        # sub_cat_id = sub_cat_id if sub_cat_id>0 else s.query(func.min(Prod_sub_cat.prod_cat_id).label('min')).first().min
        # prod_cat_sub = s.query(Prod_sub_cat).filter_by(prod_cat_sub_id=sub_cat_id).first()
        query_base = BaseQuery(Quote_system,s).filter(Quote_system.user_id==current_user.user_id)
        # quote_list = query_base.filter(or_(*([Quote_system.prod_name.like(w) for w in like_words]+
        #                                       [Quote_system.imprint_info.like(w) for w in like_words]+
        #                                       [Quote_system.special_instruction.like(w) for w in like_words]+
        #                                       [Quote_system.colors.like(w) for w in like_words]+
        #                                       [Quote_system.user_perfer_comment.like(w) for w in like_words]
        #                                      +[Quote_system.supplier_perfer_comment.like(w) for w in like_words]
        #                                      +[Quote_system.quote_id.like(w) for w in like_words]
        #                                     ))).paginate(page,customer_config.USER_QUOTE_PER_PAGE, False)
        #
        # pagination = Pagination(page=page, total=quote_list.total,
        #                         search=None, css_framework='bootstrap3',
        #                         record_name='Prod Information',
        #                         per_page=customer_config.PROD_NUM_PER_PAGE)
        quote_list,pagination = quote_search_filter(key_words,query_base,page)
        return render_template('user_temp/my_quotes.html',
                               key_words = key_words,
                               type = 'search',
                               # supplier_list = supplier_list,
                               # active_supplier = supplier_id,
                               quote_list=quote_list,
                               pagination=pagination)
    else:
        flash("Please provide key words when you search something","warning")
        return redirect(url_for("userRoute.user_quotes",type="ongoing"))