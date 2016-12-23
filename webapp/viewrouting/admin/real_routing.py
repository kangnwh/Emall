# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, flash, request
from flask import render_template, redirect,jsonify
from flask_paginate import Pagination
from flask_sqlalchemy import BaseQuery

import webapp.config.customer_config  as customer_config
from webapp.Models.db_basic import Session
from webapp.Models.prod_cat import Prod_cat
from webapp.Models.supplier import Supplier
from webapp.Models.prod_info import Prod_info
from webapp.Models.prod_pic_info import Prod_pic_info
from webapp.Models.prod_price_range import Prod_price_range
from webapp.Models.prod_profit_rate import Prod_profit_rate
from webapp.Models.prod_sub_cat import Prod_sub_cat
from webapp.Models.user import User
from webapp.common import generate_md5, admin_check, generate_sidebar,saveImage
from webapp.viewrouting.admin.forms.category_forms import DeleteLevelOneForm, CreateNewLevelOneForm, UpdateLevelOneForm,\
    DeleteLevelTwoForm, CreateNewLevelTwoForm, UpdateLevelTwoForm
# from webapp.viewrouting.admin.forms.production_forms import AddNewProduction, DeleteProduction, UpdateProduction,CreateNewProfitRateForm,\
from webapp.viewrouting.admin.forms.production_forms import CreateNewProfitRateForm,UpdateProfitRateForm,DeleteProfitRateForm
from webapp.viewrouting.admin.forms.user_forms import CreateNewForm, DeleteUserForm, UpdateUserForm, ResetPassForm

adminRoute = Blueprint('adminRoute', __name__,
                       template_folder='templates', static_folder='static')


@admin_check
def _index():
    return render_template('admin_temp/index.html')


@admin_check
def _account_management():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)
    udpate_user_form = UpdateUserForm()
    create_new_form = CreateNewForm()
    delete_user_form = DeleteUserForm()
    reset_password_form = ResetPassForm()
    s = Session()
    user_list = BaseQuery(User,s).order_by(User.user_create_ts.desc()).paginate(page, customer_config.USER_NUM_PER_PAGE, False)
    s.close
    pagination = Pagination(page=page, total=user_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='User Information',
                            per_page=customer_config.USER_NUM_PER_PAGE)

    return render_template('admin_temp/account_management.html',
                           user_list=user_list,
                           udpate_user_form=udpate_user_form,
                           delete_user_form=delete_user_form,
                           reset_password_form=reset_password_form,
                           create_new_form=create_new_form,
                           pagination=pagination)

@admin_check
def _supplier_management():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get('page', type=int, default=1)
    s = Session()
    supplier_list = BaseQuery(Supplier,s).order_by(Supplier.supplier_create_ts.desc()).paginate(page, customer_config.USER_NUM_PER_PAGE, False)
    s.close
    pagination = Pagination(page=page, total=supplier_list.total,
                            search=search, css_framework='bootstrap3',
                            record_name='Supplier Information',
                            per_page=customer_config.USER_NUM_PER_PAGE)

    return render_template('admin_temp/supplier_management.html',
                           supplier_list=supplier_list,
                           pagination=pagination)


@admin_check
def _update_supplier():
    supplier_id = request.form.get('supplier_id')
    valid_flg=request.form.get('valid_flg')
    if supplier_id:
        s = Session()
        s.query(Supplier).filter_by(supplier_id=supplier_id).update(
                {
                    "valid_flg": valid_flg
                }
        )
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for update supplier',category='danger')
        return jsonify(result='failed')

@admin_check
def _reset_supp_passwd():
    supplier_id = request.form.get('supplier_id')
    email=request.form.get('email')
    password = generate_md5(email)
    print(supplier_id)
    print(email)
    if supplier_id:
        s = Session()
        s.query(Supplier).filter_by(supplier_id=supplier_id).update(
                {
                    "password": password
                }
        )
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('Reset Password error',category='danger')
        return jsonify(result='failed')

@admin_check
def _prod_cate_mgt():
    delete_level_one_form = DeleteLevelOneForm()
    create_level_one_form = CreateNewLevelOneForm()
    update_level_one_form = UpdateLevelOneForm()

    delete_level_two_form = DeleteLevelTwoForm()
    create_level_two_form = CreateNewLevelTwoForm()
    update_level_two_form = UpdateLevelTwoForm()

    s = Session()
    level_one_list = s.query(Prod_cat).order_by(Prod_cat.prod_cat_order).all()
    level_one_all = [(i.prod_cat_id, i.prod_cat_name) for i in level_one_list]
    create_level_two_form.prod_cat_id.choices = level_one_all
    update_level_two_form.prod_cat_id.choices = level_one_all

    return render_template('admin_temp/prod_cate_mgt.html',
                           level_one_list=level_one_list,
                           delete_level_one_form=delete_level_one_form,
                           create_level_one_form=create_level_one_form,
                           update_level_one_form=update_level_one_form,
                           delete_level_two_form=delete_level_two_form,
                           create_level_two_form=create_level_two_form,
                           update_level_two_form=update_level_two_form)


@admin_check
def _spec_links():
    return render_template('admin_temp/spec_links.html')


@admin_check
def _delete_user():
    user_id = request.form.get('user_id')
    print(user_id)
    if user_id:
        s = Session()
        s.query(User).filter_by(user_id=user_id).delete()
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for delete user',category='danger')
        return jsonify(result='failed')


@admin_check
def _add_user():
    create_user_form = CreateNewForm()
    if create_user_form.validate_on_submit():
        u = User()
        u.user_name = create_user_form.user_name.data
        u.email = create_user_form.email.data
        u.password = generate_md5(create_user_form.password.data)
        u.valid_flg = 1
        u.is_paid = 0
        u.credit_points = 0
        u.is_subscribe = create_user_form.is_subscribe.data
        u.is_admin = create_user_form.is_admin.data

        s = Session()
        s.add(u)
        s.commit()
        s.close()
    else:
        flash(create_user_form.errors, category='danger')
    return redirect(url_for('adminRoute.account_management'))


@admin_check
def _update_user():
    user_id = request.form.get('user_id')
    is_admin=request.form.get('is_admin')
    valid_flg=request.form.get('valid_flg')
    if user_id:
        s = Session()
        s.query(User).filter_by(user_id=user_id).update(
                {
                    "is_admin": is_admin,
                    "valid_flg": valid_flg
                }
        )
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for update user',category='danger')
        return jsonify(result='failed')


@admin_check
@admin_check
def _delete_user():
    user_id = request.form.get('user_id')
    print(user_id)
    if user_id:
        s = Session()
        s.query(User).filter_by(user_id=user_id).delete()
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for delete user',category='danger')
        return jsonify(result='failed')


@admin_check
def _add_level_one():
    create_level_one_form = CreateNewLevelOneForm()
    if create_level_one_form.validate_on_submit():
        level_one = Prod_cat()
        level_one.prod_cat_name = create_level_one_form.prod_cat_name.data
        level_one.prod_cat_desc = create_level_one_form.prod_cat_desc.data
        level_one.prod_cat_order=create_level_one_form.prod_cat_order.data
        level_one.valid_flg = 1
        s = Session()
        s.add(level_one)
        s.commit()
        s.close()
        generate_sidebar()
    else:
        flash(create_level_one_form.errors, category='danger')
    return redirect(url_for('adminRoute.prod_cate_mgt'))


@admin_check
def _update_level_one():
    update_level_one_form = UpdateLevelOneForm()

    if update_level_one_form.validate_on_submit():
        id = update_level_one_form.prod_cat_id.data
        name = update_level_one_form.prod_cat_name.data
        desc = update_level_one_form.prod_cat_desc.data
        order_num = update_level_one_form.prod_cat_order.data
        valid_flg = update_level_one_form.valid_flg.data

        s = Session()
        s.query(Prod_cat).filter_by(prod_cat_id=id).update(
                {
                    "prod_cat_name": name,
                    "prod_cat_desc": desc,
                    'prod_cat_order': order_num,
                    "valid_flg": valid_flg
                }
        )
        s.commit()
        s.close()
        generate_sidebar()
    else:
        flash(update_level_one_form.errors, category='danger')
    return redirect(url_for('adminRoute.prod_cate_mgt'))


@admin_check
def _delete_level_one():
    delete_levelone_form = DeleteLevelOneForm()
    if delete_levelone_form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        prod_cat_id = delete_levelone_form.prod_cat_id.data

        s = Session()
        s.query(Prod_cat).filter_by(prod_cat_id=prod_cat_id).delete()
        s.commit()
        s.close()
        generate_sidebar()
    else:
        flash(delete_levelone_form.errors, category='danger')
    return redirect(url_for('adminRoute.prod_cate_mgt'))


@admin_check
def _add_level_two():
    create_level_two_form = CreateNewLevelTwoForm()
    s = Session()
    level_one_all = s.query(Prod_cat).filter_by(valid_flg=1).all()
    create_level_two_form.prod_cat_id.choices = [(i.prod_cat_id, i.prod_cat_name) for i in level_one_all]

    if create_level_two_form.validate_on_submit():
        level_two = Prod_sub_cat()
        level_two.prod_cat_sub_name = create_level_two_form.prod_cat_sub_name.data
        level_two.prod_cat_id = create_level_two_form.prod_cat_id.data
        level_two.prod_cat_sub_desc = create_level_two_form.prod_cat_sub_desc.data
        level_two.valid_flg = 1

        s = Session()
        s.add(level_two)
        s.commit()
        s.close()
        generate_sidebar()
    else:

        flash(create_level_two_form.errors, category='danger')
    return redirect(url_for('adminRoute.prod_cate_mgt'))


@admin_check
def _update_level_two():
    update_level_tow_form = UpdateLevelTwoForm()
    s = Session()
    level_one_all = s.query(Prod_cat).filter_by(valid_flg=1).all()
    update_level_tow_form.prod_cat_id.choices = [(i.prod_cat_id, i.prod_cat_name) for i in level_one_all]

    if update_level_tow_form.validate_on_submit():
        id = update_level_tow_form.prod_cat_sub_id.data
        name = update_level_tow_form.prod_cat_sub_name.data
        desc = update_level_tow_form.prod_cat_sub_desc.data
        valid_flg = update_level_tow_form.valid_flg.data
        parent_id = update_level_tow_form.prod_cat_id.data

        s = Session()
        s.query(Prod_sub_cat).filter_by(prod_cat_sub_id=id).update(
                {
                    "prod_cat_sub_name": name,
                    'prod_cat_id': parent_id,
                    "prod_cat_sub_desc": desc,
                    "valid_flg": valid_flg
                }
        )
        s.commit()
        s.close()
        generate_sidebar()
    else:
        flash(update_level_tow_form.errors, category='danger')
    return redirect(url_for('adminRoute.prod_cate_mgt'))


@admin_check
def _delete_level_two():
    delete_level_two_form = DeleteLevelTwoForm()
    if delete_level_two_form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        prod_cat_sub_id = delete_level_two_form.prod_cat_sub_id.data

        s = Session()
        s.query(Prod_sub_cat).filter_by(prod_cat_sub_id=prod_cat_sub_id).delete()
        s.commit()
        s.close()
        generate_sidebar()
    else:
        flash(delete_level_two_form.errors, category='danger')
    return redirect(url_for('adminRoute.prod_cate_mgt'))


@admin_check
def _reset_password():
    reset_password_form = ResetPassForm()

    if reset_password_form.validate_on_submit():
        user_id = reset_password_form.user_id.data
        # email=reset_password_form.email.data
        password = generate_md5(reset_password_form.email.data)

        s = Session()
        s.query(User).filter_by(user_id=user_id).update(
                {
                    "password": password
                }
        )
        s.commit()
        s.close()
    else:
        flash(reset_password_form.errors, category='danger')
    return redirect(url_for('adminRoute.account_management'))

#
# @admin_check
# def _publish_prod():
#     delete_form = DeleteProduction()
#     add_form = AddNewProduction()
#     update_form = UpdateProduction()
#
#     s = Session()
#     prod_list = s.query(Prod_info).filter_by(valid_flg=1).all()
#     sub_category = s.query(Prod_sub_cat).filter_by(valid_flg=1).order_by(Prod_sub_cat.prod_cat_sub_id).all()
#     sub_category_list = [(i.prod_cat_sub_id, i.prod_cat_sub_name) for i in sub_category]
#
#     add_form.prod_cat_sub_id.choices = sub_category_list
#
#     return render_template('admin_temp/publish_prod.html',
#                            prod_list=prod_list,
#                            delete_form=delete_form,
#                            add_form=add_form,
#                            update_form=update_form)
#
#
# @admin_check
# def _add_new_prod():
#     add_form = AddNewProduction()
#     s = Session()
#     sub_category = s.query(Prod_sub_cat).filter_by(valid_flg=1).order_by(Prod_sub_cat.prod_cat_sub_name).all()
#     sub_category_list = [(i.prod_cat_sub_id, i.prod_cat_sub_name) for i in sub_category]
#     add_form.prod_cat_sub_id.choices = sub_category_list
#     s.close()
#
#     if add_form.validate_on_submit():
#         prod = Prod_info()
#         prod.prod_name = add_form.prod_name.data
#         prod.prod_desc = add_form.prod_desc.data
#         prod.lead_time = add_form.lead_time.data
#         prod.prod_size = add_form.prod_size.data
#         prod.imprint_size = add_form.imprint_size.data
#         prod.price_basis = add_form.price_basis.data
#         prod.valid_flg = 1  # add_form.valid_flg.data
#         prod.prod_cat_sub_id = add_form.prod_cat_sub_id.data
#         prod.colors = add_form.colors.data
#
#         price_range = Prod_price_range()
#
#         #Price range
#         price_range.quantity_from1 = add_form.quantity_from1.data
#         price_range.quantity_to1 = add_form.quantity_to1.data
#         price_range.unit_price1 = add_form.unit_price1.data
#         price_range.imprinting_prices1 = add_form.imprinting_prices1.data
#         price_range.setup_cost1 = add_form.setup_cost1.data
#         price_range.freight_cost1 = add_form.freight_cost1.data
#
#         price_range.quantity_from2 = add_form.quantity_from2.data
#         price_range.quantity_to2 = add_form.quantity_to2.data
#         price_range.unit_price2 = add_form.unit_price2.data
#         price_range.imprinting_prices2 = add_form.imprinting_prices2.data
#         price_range.setup_cost2 = add_form.setup_cost2.data
#         price_range.freight_cost2 = add_form.freight_cost2.data
#
#         price_range.quantity_from3 = add_form.quantity_from3.data
#         price_range.quantity_to3 = add_form.quantity_to3.data
#         price_range.unit_price3 = add_form.unit_price3.data
#         price_range.imprinting_prices3 = add_form.imprinting_prices3.data
#         price_range.setup_cost3 = add_form.setup_cost3.data
#         price_range.freight_cost3 = add_form.freight_cost3.data
#
#         price_range.quantity_from4 = add_form.quantity_from4.data
#         price_range.quantity_to4 = add_form.quantity_to4.data
#         price_range.unit_price4 = add_form.unit_price4.data
#         price_range.imprinting_prices4 = add_form.imprinting_prices4.data
#         price_range.setup_cost4 = add_form.setup_cost4.data
#         price_range.freight_cost4 = add_form.freight_cost4.data
#
#         price_range.quantity_from5 = add_form.quantity_from5.data
#         price_range.quantity_to5 = add_form.quantity_to5.data
#         price_range.unit_price5 = add_form.unit_price5.data
#         price_range.imprinting_prices5 = add_form.imprinting_prices5.data
#         price_range.setup_cost5 = add_form.setup_cost5.data
#         price_range.freight_cost5 = add_form.freight_cost5.data
#
#         #map prod and price_range
#         prod.price_ranges = [price_range]
#
#         #map prod and picture
#         prod.prod_pics=[]
#
#         #Pictures
#         cover_img_file = request.files['cover_img_file']
#         filename = saveImage(cover_img_file,prod)
#         prod.cover_img = filename if filename else 'default.png'
#
#
#         #extra file list
#         extra_imgs = request.files.getlist('extra_img_file')
#         extra_descs =request.form.getlist('extra_img_desc')#request.form.getlist('extra_img_desc')
#
#         for i in range(extra_imgs.__len__()):
#             e_i_picture = Prod_pic_info()
#             e_i_filename = saveImage(extra_imgs[i],prod)
#             if e_i_filename:
#                 e_i_picture.image_path = e_i_filename
#                 e_i_picture.img_desc = extra_descs[i]
#                 e_i_picture.valid_flg = 1
#                 prod.prod_pics.append(e_i_picture)
#
#
#
#
#         s = Session()
#         s.merge(prod)
#         s.commit()
#         s.close()
#         message = "Add production {name} successfully!".format(name=prod.prod_name)
#         flash(message,category='success')
#
#     elif request.method == 'POST':
#
#         flash(add_form.errors, category='danger')
#
#     else:
#         pass
#     return render_template("admin_temp/add_prod_form.html",add_form=add_form)
#
#
# @admin_check
# def _update_prod():
#     update_form = UpdateProduction()
#     s = Session()
#     sub_category = s.query(Prod_sub_cat).filter_by(valid_flg=1).order_by(Prod_sub_cat.prod_cat_sub_name).all()
#     sub_category_list = [(i.prod_cat_sub_id, i.prod_cat_sub_name) for i in sub_category]
#     update_form.prod_cat_sub_id.choices = sub_category_list
#
#     if update_form.validate_on_submit():
#         prod = Prod_info()
#         prod.prod_id = update_form.prod_id.data
#         this_prod = s.query(Prod_info).filter_by(prod_id=prod.prod_id).first()
#         prod.prod_name = update_form.prod_name.data
#         prod.prod_desc = update_form.prod_desc.data
#         prod.lead_time = update_form.lead_time.data
#         prod.prod_size = update_form.prod_size.data
#         prod.imprint_size = update_form.imprint_size.data
#         prod.price_basis = update_form.price_basis.data
#         prod.valid_flg = 1 if update_form.valid_flg.data else 0 # add_form.valid_flg.data
#         prod.prod_cat_sub_id = update_form.prod_cat_sub_id.data
#         prod.colors = update_form.colors.data
#
#         price_range = Prod_price_range()
#
#         #Price range
#         price_range.quantity_from1 = update_form.quantity_from1.data
#         price_range.quantity_to1 = update_form.quantity_to1.data
#         price_range.unit_price1 = update_form.unit_price1.data
#         price_range.imprinting_prices1 = update_form.imprinting_prices1.data
#         price_range.setup_cost1 = update_form.setup_cost1.data
#         price_range.freight_cost1 = update_form.freight_cost1.data
#
#         price_range.quantity_from2 = update_form.quantity_from2.data
#         price_range.quantity_to2 = update_form.quantity_to2.data
#         price_range.unit_price2 = update_form.unit_price2.data
#         price_range.imprinting_prices2 = update_form.imprinting_prices2.data
#         price_range.setup_cost2 = update_form.setup_cost2.data
#         price_range.freight_cost2 = update_form.freight_cost2.data
#
#         price_range.quantity_from3 = update_form.quantity_from3.data
#         price_range.quantity_to3 = update_form.quantity_to3.data
#         price_range.unit_price3 = update_form.unit_price3.data
#         price_range.imprinting_prices3 = update_form.imprinting_prices3.data
#         price_range.setup_cost3 = update_form.setup_cost3.data
#         price_range.freight_cost3 = update_form.freight_cost3.data
#
#         price_range.quantity_from4 = update_form.quantity_from4.data
#         price_range.quantity_to4 = update_form.quantity_to4.data
#         price_range.unit_price4 = update_form.unit_price4.data
#         price_range.imprinting_prices4 = update_form.imprinting_prices4.data
#         price_range.setup_cost4 = update_form.setup_cost4.data
#         price_range.freight_cost4 = update_form.freight_cost4.data
#
#         price_range.quantity_from5 = update_form.quantity_from5.data
#         price_range.quantity_to5 = update_form.quantity_to5.data
#         price_range.unit_price5 = update_form.unit_price5.data
#         price_range.imprinting_prices5 = update_form.imprinting_prices5.data
#         price_range.setup_cost5 = update_form.setup_cost5.data
#         price_range.freight_cost5 = update_form.freight_cost5.data
#
#         #map prod and price_range
#         prod.price_ranges = [price_range]
#
#         #map prod and picture
#         prod.prod_pics=[]
#
#         #Pictures
#
#         # cover_img_file = request.files['cover_img_file']
#         # if  cover_img_file.filename :
#         #     if allowed_file(cover_img_file.filename):
#         #             filename = "{prod_name}{time}.{ext}".format( prod_name=prod.prod_name ,
#         #                                                          time=datetime.datetime.now().isoformat().replace(':','_').replace('.','_') ,
#         #                                                          ext=secure_filename(cover_img_file.filename)[-3:])
#         #             prod.cover_img = filename #os.path.join(PROD_UPLOAD_PATH, filename)
#         #             cover_img_file.save(os.path.join(PROD_UPLOAD_PATH, filename))
#         #     else :
#         #             flash("Only accept {types} file".format(types=ALLOWED_EXTENSIONS),category='danger')
#         #             prod.cover_img = this_prod.cover_img
#         # else:
#         #     prod.cover_img = this_prod.cover_img
#
#         cover_img_file = request.files['cover_img_file']
#         filename = saveImage(cover_img_file,prod)
#         prod.cover_img = filename if filename else this_prod.cover_img
#
#         #append new extra file list
#         extra_imgs = request.files.getlist('extra_img_file')
#         extra_descs =request.form.getlist('extra_img_desc')
#         for i in range(extra_imgs.__len__()):
#             e_i_picture = Prod_pic_info()
#             # e_i_filename = "{prod_name}{time}.{ext}".format( prod_name=prod.prod_name ,
#             #                                                  time=datetime.datetime.now().isoformat().replace(':','_').replace('.','_'),
#             #                                                  ext=secure_filename(extra_imgs[i].filename)[-3:])
#             # e_i_picture.image_path = e_i_filename    #os.path.join(PROD_UPLOAD_PATH, e_i_filename)
#             # extra_imgs[i].save(os.path.join(PROD_UPLOAD_PATH, e_i_filename))
#             #
#             # e_i_picture.img_desc = extra_descs[i]
#             # e_i_picture.valid_flg = 1
#             # prod.prod_pics.append(e_i_picture)
#
#             e_i_filename = saveImage(extra_imgs[i],prod)
#             if e_i_filename:
#                 e_i_picture.image_path = e_i_filename
#                 e_i_picture.img_desc = extra_descs[i]
#                 e_i_picture.valid_flg = 1
#                 prod.prod_pics.append(e_i_picture)
#
#         #append existing extra file list
#         for p in this_prod.prod_pics:
#             existing_extra_pic = Prod_pic_info()
#             existing_extra_pic.img_desc=p.img_desc
#             existing_extra_pic.image_path=p.image_path
#             existing_extra_pic.valid_flg=1
#             prod.prod_pics.append(existing_extra_pic)
#
#
#         #s = Session()
#         s.commit()
#         s.query(Prod_info).filter_by(prod_id=this_prod.prod_id).delete()
#         s.flush()
#         s.merge(prod)
#         message = "Update production {name} successfully!".format(name=prod.prod_name)
#         s.commit()
#         flash(message,category='info')
#         return redirect(url_for('adminRoute.update_prod',prod_id=prod.prod_id))
#     elif request.method == 'POST':
#
#         flash(update_form.errors, category='danger')
#
#     else:
#         prod_id = request.args.get('prod_id', 1) if request.method == 'GET' else request.form.get('prod_id', 1)
#         this_prod = s.query(Prod_info).filter_by(prod_id=prod_id).first()
#         this_prod.price_ranges = this_prod.price_ranges if this_prod.price_ranges.__len__()>0 else [Prod_price_range()]
#
#     return render_template("admin_temp/update_prod_form.html",
#                            update_form=update_form,
#                            this_prod=this_prod)
#
# @admin_check
# def _delete_prod():
#     prod_id = request.form.get('prod_id')
#     print(prod_id)
#     if prod_id:
#         s = Session()
#         s.query(Prod_info).filter_by(prod_id=prod_id).delete()
#         s.commit()
#         s.close()
#         return jsonify(result='succ')
#     else:
#         flash('No Valid information for delete production',category='danger')
#         return jsonify(result='failed')
#
# @admin_check
# def _delete_cover_page():
#     prod_id = request.form.get('prod_id')
#     if prod_id:
#         s = Session()
#         s.query(Prod_info).filter_by(prod_id=prod_id).update({
#             'cover_img' : 'default.png'
#         })
#         s.commit()
#         s.close()
#         return jsonify(result='succ')
#     else:
#         flash('No Valid information for delete coverage image',category='danger')
#         return '<HTML><h2>No Valid information for delete coverage image</h2></HTML>'
#
# @admin_check
# def _delete_extra_pics():
#     prod_pic_id = request.form.get('prod_pic_id')
#     if prod_pic_id:
#         s = Session()
#         s.query(Prod_pic_info).filter_by(prod_pic_id=prod_pic_id).delete()
#         s.commit()
#         s.close()
#         return jsonify(result='succ')
#     else:
#         flash('No Valid information for delete coverage image',category='danger')
#         return '<HTML><h2>No Valid information for delete coverage image</h2></HTML>'


@admin_check
def _manage_profit_rate():
    udpate_profit_rate_form = UpdateProfitRateForm()
    create_new_rate_form = CreateNewProfitRateForm()
    delete_new_rate_form=DeleteProfitRateForm()
    s = Session()
    profit_list = s.query(Prod_profit_rate)
    return render_template('admin_temp/manage_profit_rate.html',
                           profit_list=profit_list,
                           udpate_profit_rate_form=udpate_profit_rate_form,
                           delete_new_rate_form=delete_new_rate_form,
                           create_new_rate_form=create_new_rate_form)


@admin_check
def _add_profit():
    create_new_rate_form = CreateNewProfitRateForm()
    if create_new_rate_form.validate_on_submit():
        p = Prod_profit_rate()
        p.profit_rate = create_new_rate_form.profit_rate.data
        p.valid_flg = create_new_rate_form.valid_flg.data
        s = Session()
        s.add(p)
        s.commit()
        s.close()
    else:
        flash(create_new_rate_form.errors, category='danger')
    return redirect(url_for('adminRoute.manage_profit_rate'))


@admin_check
def _update_profit():
    udpate_profit_rate_form = UpdateProfitRateForm()
    if udpate_profit_rate_form.validate_on_submit():
        profit_id = udpate_profit_rate_form.profit_id.data
        valid_flg = udpate_profit_rate_form.valid_flg.data
        profit_rate = udpate_profit_rate_form.profit_rate.data

        s = Session()
        s.query(Prod_profit_rate).filter_by(profit_id=profit_id).update(
                {
                    "valid_flg": valid_flg,
                    "profit_rate": profit_rate
                }
        )
        s.commit()
        s.close()
    else:
        flash(udpate_profit_rate_form.errors, category='danger')
    return redirect(url_for('adminRoute.manage_profit_rate'))


@admin_check
def _delete_profit():
    delete_new_rate_form=DeleteProfitRateForm()
    if delete_new_rate_form.validate_on_submit():
        profit_id = delete_new_rate_form.profit_id.data

        s = Session()
        s.query(Prod_profit_rate).filter_by(profit_id=profit_id).delete()
        s.commit()
        s.close()

    return redirect(url_for('adminRoute.manage_profit_rate'))

