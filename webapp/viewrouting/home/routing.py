# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, flash, request, abort
from flask import render_template, redirect
from werkzeug import secure_filename
from webapp.Models.db_basic import Session
from webapp.Models.prod_sub_cat import Prod_sub_cat
from webapp.Models.prod_info import Prod_info
from webapp.Models.prod_pic_info import Prod_pic_info
from flask_login import current_user, login_required
from webapp.viewrouting.home.forms.home_forms import UserFeedbackForm,UploadUserLogoForm
from webapp.viewrouting.admin.forms.production_forms import UpdateProduction
from webapp.Models.user_feedback import User_feedback
from webapp.Models.user import User
from webapp.Models.v_prod_price_range import V_Prod_price_range
from flask_sqlalchemy import BaseQuery
from sqlalchemy import func
from flask_paginate import Pagination
import webapp.customer_config  as customer_config
from webapp.common import allowed_file,generatePNG
import os

homeRoute = Blueprint('homeRoute', __name__,
                      template_folder='templates', static_folder='static')


@homeRoute.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home_temp/index.html')


@homeRoute.route('/Free_Shipping', methods=['GET', 'POST'])
def Free_Shipping():
    return render_template('home_temp/Free_Shipping.html')


@homeRoute.route('/document', methods=['GET', 'POST'])
def document():
    return render_template('home_temp/document.html')


@homeRoute.route('/User_Feedback', methods=['GET', 'POST'])
@login_required
def User_Feedback():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)
    s1 = Session()
    user_feedback_list = BaseQuery(User_feedback,s1).order_by(User_feedback.user_comment_ts.desc()).paginate(page,customer_config.PROD_NUM_PER_PAGE,False)
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
        prod_list = BaseQuery(Prod_info,s).filter_by(prod_cat_sub_id=sub_cat_id).paginate(page,customer_config.PROD_NUM_PER_PAGE,False)
    else:
        prod_list = BaseQuery(Prod_info,s).filter_by(valid_flg=1,prod_cat_sub_id=sub_cat_id).paginate(page,customer_config.PROD_NUM_PER_PAGE,False)

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
    s.close
    return render_template('home_temp/indiv_prod.html',
                           this_prod=this_prod)

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

@homeRoute.route('/sendmail/<to>')
def sendtest(to):
    from webapp.common.mails import send_email_indiv
    send_email_indiv("This is a testing flask mail ", [to], 'Test body', "<h1> Hello Flask Email </h1>")
    render_template("home_temp/index.html")