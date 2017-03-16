# -*- coding: utf-8 -*-
import os

from flask import Blueprint, flash, request, render_template,url_for,redirect
from flask_login import current_user, login_required
from flask_paginate import Pagination
from flask_sqlalchemy import BaseQuery
from sqlalchemy import func,or_,and_
from werkzeug import secure_filename

import webapp.config.customer_config  as customer_config
from webapp.Models.db_basic import Session
from webapp.Models.prod_info import Prod_info
from webapp.Models.prod_sub_cat import Prod_sub_cat
from webapp.Models.v_hot_prods import V_hot_prods
from webapp.Models.user import User
from webapp.Models.user_feedback import User_feedback
from webapp.Models.compliment_system import Compliment_system
from webapp.common import allowed_file,generatePNG,prod_search_filter
from webapp.common.mails import send_email_base,send_advertisement
from webapp.viewrouting.home.forms.home_forms import UserFeedbackForm

homeRoute = Blueprint('homeRoute', __name__,
                      template_folder='templates', static_folder='static')


@homeRoute.route('/', methods=['GET', 'POST'])
def index():

    return render_template('home_temp/index.html')


@homeRoute.route('/Free_Shipping', methods=['GET', 'POST'])
def Free_Shipping():
    return render_template('home_temp/Free_Shipping.html')


@homeRoute.route('/hot_prods', methods=['GET', 'POST'])
def hot_prods():
    search = False
    page = request.args.get('page', type=int, default=1)

    s = Session()

    prod_list = BaseQuery(Prod_info,s).filter_by(valid_flg=1,approve_stat=1).paginate(page,customer_config.PROD_NUM_PER_PAGE, False)

    pagination = Pagination(page=page, total=prod_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Prod Information',
                            per_page=customer_config.PROD_NUM_PER_PAGE)

    return render_template('home_temp/sub_category_list.html',
                           sub_cat_name='Hot Productions',
                           prod_list=prod_list,
                           nav_active=None,
                           pagination=pagination)

@homeRoute.route('/clearance', methods=['GET', 'POST'])
def clearance():
    search = False
    page = request.args.get('page', type=int, default=1)

    s = Session()

    prod_list = BaseQuery(Prod_info,s).filter_by(valid_flg=1,approve_stat=1,is_clearance=1).paginate(page,customer_config.PROD_NUM_PER_PAGE, False)

    pagination = Pagination(page=page, total=prod_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Prod Information',
                            per_page=customer_config.PROD_NUM_PER_PAGE)

    return render_template('home_temp/sub_category_list.html',
                           sub_cat_name='Clearance',
                           prod_list=prod_list,
                           nav_active=None,
                           pagination=pagination)

@homeRoute.route('/on_sale', methods=['GET', 'POST'])
def on_sale():
    search = False
    page = request.args.get('page', type=int, default=1)

    s = Session()

    prod_list = BaseQuery(Prod_info,s).filter_by(valid_flg=1,approve_stat=1,is_special_price_flg=1,is_del_flg=0).paginate(page,customer_config.PROD_NUM_PER_PAGE, False)

    pagination = Pagination(page=page, total=prod_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Prod Information',
                            per_page=customer_config.PROD_NUM_PER_PAGE)

    return render_template('home_temp/sub_category_list.html',
                           sub_cat_name='On Sale!',
                           prod_list=prod_list,
                           nav_active=None,
                           pagination=pagination)

@homeRoute.route('/User_Feedback', methods=['GET', 'POST'])
@login_required
def User_Feedback():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)
    s1 = Session()
    user_feedback_list = BaseQuery(User_feedback,s1).order_by(User_feedback.user_comment_ts.desc()).paginate(page,
                                                                                                             customer_config.PROD_NUM_PER_PAGE, False)
    pagination = Pagination(page=page, total=user_feedback_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Feedback Information',
                            per_page=customer_config.FEEDBACK_NUM_PER_PAGE)
    user_feedback_form = UserFeedbackForm()

    if user_feedback_form.validate_on_submit():
        user_feedback = User_feedback()
        user_feedback.valid_flg = 1
        user_feedback.user_id = user_feedback_form.user_id.data
        user_feedback.user_name = user_feedback_form.user_name.data
        user_feedback.email = user_feedback_form.email.data
        user_feedback.user_comment = user_feedback_form.user_comment.data
        s = Session()
        s.add(user_feedback)
        s.commit()
        s.close()
    elif request.method == 'POST':
        flash(user_feedback_form.errors, category='danger')

    return render_template('home_temp/user_feedback.html',
                           user_feedback_list=user_feedback_list,
                           user_feedback_form=user_feedback_form,
                           pagination=pagination)


@homeRoute.route('/sub-category/<int:sub_cat_id>', methods=['GET'])
def sub_category_list(sub_cat_id):
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)

    s = Session()
    sub_cat_id = sub_cat_id if sub_cat_id>0 else s.query(func.min(Prod_sub_cat.prod_cat_id).label('min')).first().min
    prod_cat_sub = s.query(Prod_sub_cat).filter_by(prod_cat_sub_id=sub_cat_id).first()

    if current_user.is_administrator:
        prod_list = BaseQuery(Prod_info,s).filter_by(prod_cat_sub_id=sub_cat_id).paginate(page,
                                                                                          customer_config.PROD_NUM_PER_PAGE, False)
    else:
        prod_list = BaseQuery(Prod_info,s).filter_by(valid_flg=1,prod_cat_sub_id=sub_cat_id,approve_stat=1).paginate(page,
                                                                                                      customer_config.PROD_NUM_PER_PAGE, False)

    pagination = Pagination(page=page, total=prod_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Prod Information',
                            per_page=customer_config.PROD_NUM_PER_PAGE)

    return render_template('home_temp/sub_category_list.html',
                           sub_cat_name=prod_cat_sub.prod_cat_sub_name,
                           prod_list=prod_list,
                           nav_active=prod_cat_sub.prod_cat_id,
                           pagination=pagination)



@homeRoute.route('/indiv_prod', methods=['GET'])
def indiv_prod():
    s = Session()
    prod_id = request.args.get('prod_id', 1)
    this_prod = s.query(Prod_info).filter_by(prod_id=prod_id).first()
    # s.close()
    return render_template('home_temp/indiv_prod.html',
                           this_prod=this_prod) , s.close()

@homeRoute.route('/upload_user_logo', methods=['GET','POST'])
@login_required
def upload_user_logo():

    if request.method == 'POST':
        user_logo_file=request.files['user_logo_file']
        if allowed_file(user_logo_file.filename):
            filename = "{user_email}.{ext}".format( user_email=current_user.email ,
                                                         ext=secure_filename(user_logo_file.filename)[-3:])
        user_logo_file.save(os.path.join(customer_config.USER_LOGO_UPLOAD_PATH, filename))
        generatePNG(filename)
        s =Session()
        s.query(User).filter_by(user_id=current_user.user_id).update({
            'logo_link':filename
        })
        s.commit()
        s.close()

    return render_template('home_temp/upload_user_logo.html',
                           allowed_files = list(customer_config.ALLOWED_EXTENSIONS))

# @homeRoute.route('/sendmail/<to>')
# def sendtest(to):
#
#     send_email_base("This is a testing flask mail ", [to], 'Test body', "<h1> Hello Flask Email </h1>")
#     return render_template("home_temp/index.html")


@homeRoute.route('/search', methods=['GET'])
#@login_required
def search():
    key_words = request.args.get("q")
    supplier_id = request.args.get("supplier")

    if key_words:

        page = request.args.get('page', type=int, default=1)
        s = Session()

        query_base = BaseQuery(Prod_info,s)

        if not current_user.is_administrator:
            query_base = query_base.filter(Prod_info.valid_flg==1,Prod_info.approve_stat==1)

        prod_list,supplier_list,pagination = prod_search_filter(key_words,query_base,page,supplier_id)
        return render_template('home_temp/search.html',
                               key_words = key_words,
                               supplier_list = supplier_list,
                               active_supplier = supplier_id,
                               prod_list=prod_list,
                               pagination=pagination)
    else:
        flash("Please provide key words when you search something","warning")
        return redirect(url_for("homeRoute.index"))


@homeRoute.route('/show_feedback/<int:prod_id>', methods=['GET'])
@login_required
def show_feedback(prod_id):
    s = Session()

    page = request.args.get('page', type=int, default=1)

    feedback = BaseQuery(Compliment_system,s).filter_by(prod_id=prod_id).order_by(Compliment_system.user_compliment_time.desc()).paginate(page,customer_config.FEEDBACK_NUM_PER_PAGE, False)

    pagination = Pagination(page=page, total=feedback.total,
                                search=False, css_framework='bootstrap3',
                                record_name='Feedback Information',
                                per_page=customer_config.FEEDBACK_NUM_PER_PAGE)

    return render_template("home_temp/show_feedback.html",
                           feedbacks = feedback,
                           pagination=pagination),s.close()