
# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, flash, request
from flask import render_template, redirect,jsonify
from flask_paginate import Pagination
from flask_sqlalchemy import BaseQuery
from flask_login import login_required,current_user
import webapp.config.customer_config  as customer_config
from webapp.Models.db_basic import Session
from webapp.Models.prod_cat import Prod_cat
from webapp.Models.prod_info import Prod_info
from webapp.Models.prod_pic_info import Prod_pic_info
from webapp.Models.prod_price_range import Prod_price_range
from webapp.Models.prod_profit_rate import Prod_profit_rate
from webapp.Models.prod_sub_cat import Prod_sub_cat

from webapp.common import saveImage

from webapp.viewrouting.admin.forms.production_forms import AddNewProduction, DeleteProduction, UpdateProduction
#from webapp.viewrouting.admin.forms.user_forms import CreateNewForm, DeleteUserForm, UpdateUserForm, ResetPassForm

supplierRoute = Blueprint('supplierRoute', __name__,
                       template_folder='templates', static_folder='static')


@supplierRoute.route("/",methods=['GET','POST'])
@login_required
def index():
    return render_template('admin_temp/index.html')

@supplierRoute.route("/account_management",methods=['GET','POST'])
@login_required
def account_management():

    return render_template('admin_temp/account_management.html')



@supplierRoute.route("/publish_prod",methods=['GET','POST'])
@login_required
def publish_prod():
    delete_form = DeleteProduction()
    add_form = AddNewProduction()
    update_form = UpdateProduction()

    s = Session()
    prod_list = s.query(Prod_info).filter_by(valid_flg=1).all()
    sub_category = s.query(Prod_sub_cat).filter_by(valid_flg=1).order_by(Prod_sub_cat.prod_cat_sub_id).all()
    sub_category_list = [(i.prod_cat_sub_id, i.prod_cat_sub_name) for i in sub_category]

    add_form.prod_cat_sub_id.choices = sub_category_list

    return render_template('admin_temp/publish_prod.html',
                           prod_list=prod_list,
                           delete_form=delete_form,
                           add_form=add_form,
                           update_form=update_form)

@supplierRoute.route("/add_new_prod",methods=['GET','POST'])
@login_required
def add_new_prod():
    add_form = AddNewProduction()
    s = Session()
    sub_category = s.query(Prod_sub_cat).filter_by(valid_flg=1).order_by(Prod_sub_cat.prod_cat_sub_name).all()
    sub_category_list = [(i.prod_cat_sub_id, i.prod_cat_sub_name) for i in sub_category]
    add_form.prod_cat_sub_id.choices = sub_category_list
    s.close()

    if add_form.validate_on_submit():
        prod = Prod_info()
        prod.prod_name = add_form.prod_name.data
        prod.prod_desc = add_form.prod_desc.data
        prod.lead_time = add_form.lead_time.data
        prod.prod_size = add_form.prod_size.data
        prod.imprint_size = add_form.imprint_size.data
        prod.price_basis = add_form.price_basis.data
        prod.valid_flg = 1  # add_form.valid_flg.data
        prod.prod_cat_sub_id = add_form.prod_cat_sub_id.data
        prod.colors = add_form.colors.data
        prod.is_special_price_flg = add_form.is_special_price_flg.data
        prod.special_price_old = add_form.special_price_old.data
        prod.special_price_new = add_form.special_price_new.data
        prod.special_price_campaign_time = add_form.special_price_campaign_time.data
        prod.is_clearance = add_form.is_clearance.data
        prod.is_new_prod = add_form.is_new_prod.data
        prod.is_patent_prod = add_form.is_patent_prod.data




        price_range = Prod_price_range()

        #Price range
        price_range.quantity_from1 = add_form.quantity_from1.data
        price_range.quantity_to1 = add_form.quantity_to1.data
        price_range.unit_price1 = add_form.unit_price1.data
        price_range.imprinting_prices1 = add_form.imprinting_prices1.data
        price_range.setup_cost1 = add_form.setup_cost1.data
        price_range.freight_cost1 = add_form.freight_cost1.data

        price_range.quantity_from2 = add_form.quantity_from2.data
        price_range.quantity_to2 = add_form.quantity_to2.data
        price_range.unit_price2 = add_form.unit_price2.data
        price_range.imprinting_prices2 = add_form.imprinting_prices2.data
        price_range.setup_cost2 = add_form.setup_cost2.data
        price_range.freight_cost2 = add_form.freight_cost2.data

        price_range.quantity_from3 = add_form.quantity_from3.data
        price_range.quantity_to3 = add_form.quantity_to3.data
        price_range.unit_price3 = add_form.unit_price3.data
        price_range.imprinting_prices3 = add_form.imprinting_prices3.data
        price_range.setup_cost3 = add_form.setup_cost3.data
        price_range.freight_cost3 = add_form.freight_cost3.data

        price_range.quantity_from4 = add_form.quantity_from4.data
        price_range.quantity_to4 = add_form.quantity_to4.data
        price_range.unit_price4 = add_form.unit_price4.data
        price_range.imprinting_prices4 = add_form.imprinting_prices4.data
        price_range.setup_cost4 = add_form.setup_cost4.data
        price_range.freight_cost4 = add_form.freight_cost4.data

        price_range.quantity_from5 = add_form.quantity_from5.data
        price_range.quantity_to5 = add_form.quantity_to5.data
        price_range.unit_price5 = add_form.unit_price5.data
        price_range.imprinting_prices5 = add_form.imprinting_prices5.data
        price_range.setup_cost5 = add_form.setup_cost5.data
        price_range.freight_cost5 = add_form.freight_cost5.data

        #map prod and price_range
        prod.price_ranges = [price_range]

        #map prod and picture
        prod.prod_pics=[]

        #Pictures
        cover_img_file = request.files['cover_img_file']
        filename = saveImage(cover_img_file,prod)
        prod.cover_img = filename if filename else 'default.png'


        #extra file list
        extra_imgs = request.files.getlist('extra_img_file')
        extra_descs =request.form.getlist('extra_img_desc')#request.form.getlist('extra_img_desc')

        for i in range(extra_imgs.__len__()):
            e_i_picture = Prod_pic_info()
            e_i_filename = saveImage(extra_imgs[i],prod)
            if e_i_filename:
                e_i_picture.image_path = e_i_filename
                e_i_picture.img_desc = extra_descs[i]
                e_i_picture.valid_flg = 1
                prod.prod_pics.append(e_i_picture)



        prod.supplier_id = current_user.supplier_id

        s = Session()
        s.merge(prod)
        s.commit()
        s.close()
        message = "Add production {name} successfully!".format(name=prod.prod_name)
        flash(message,category='success')

    elif request.method == 'POST':

        flash(add_form.errors, category='danger')

    else:
        pass
    return render_template("admin_temp/add_prod_form.html",add_form=add_form)



@supplierRoute.route("/update_prod",methods=['GET','POST'])
@login_required
def update_prod():
    update_form = UpdateProduction()
    s = Session()
    sub_category = s.query(Prod_sub_cat).filter_by(valid_flg=1).order_by(Prod_sub_cat.prod_cat_sub_name).all()
    sub_category_list = [(i.prod_cat_sub_id, i.prod_cat_sub_name) for i in sub_category]
    update_form.prod_cat_sub_id.choices = sub_category_list

    if update_form.validate_on_submit():
        prod = Prod_info()
        prod.prod_id = update_form.prod_id.data
        this_prod = s.query(Prod_info).filter_by(prod_id=prod.prod_id).first()
        prod.prod_name = update_form.prod_name.data
        prod.prod_desc = update_form.prod_desc.data
        prod.lead_time = update_form.lead_time.data
        prod.prod_size = update_form.prod_size.data
        prod.imprint_size = update_form.imprint_size.data
        prod.price_basis = update_form.price_basis.data
        prod.valid_flg = 1 if update_form.valid_flg.data else 0 # add_form.valid_flg.data
        prod.prod_cat_sub_id = update_form.prod_cat_sub_id.data
        prod.colors = update_form.colors.data
        prod.is_special_price_flg = update_form.is_special_price_flg.data
        prod.special_price_old = update_form.special_price_old.data
        prod.special_price_new = update_form.special_price_new.data
        prod.special_price_campaign_time = update_form.special_price_campaign_time.data
        prod.is_clearance = update_form.is_clearance.data
        prod.is_new_prod = update_form.is_new_prod.data
        prod.is_patent_prod = update_form.is_patent_prod.data

        price_range = Prod_price_range()

        #Price range
        price_range.quantity_from1 = update_form.quantity_from1.data
        price_range.quantity_to1 = update_form.quantity_to1.data
        price_range.unit_price1 = update_form.unit_price1.data
        price_range.imprinting_prices1 = update_form.imprinting_prices1.data
        price_range.setup_cost1 = update_form.setup_cost1.data
        price_range.freight_cost1 = update_form.freight_cost1.data

        price_range.quantity_from2 = update_form.quantity_from2.data
        price_range.quantity_to2 = update_form.quantity_to2.data
        price_range.unit_price2 = update_form.unit_price2.data
        price_range.imprinting_prices2 = update_form.imprinting_prices2.data
        price_range.setup_cost2 = update_form.setup_cost2.data
        price_range.freight_cost2 = update_form.freight_cost2.data

        price_range.quantity_from3 = update_form.quantity_from3.data
        price_range.quantity_to3 = update_form.quantity_to3.data
        price_range.unit_price3 = update_form.unit_price3.data
        price_range.imprinting_prices3 = update_form.imprinting_prices3.data
        price_range.setup_cost3 = update_form.setup_cost3.data
        price_range.freight_cost3 = update_form.freight_cost3.data

        price_range.quantity_from4 = update_form.quantity_from4.data
        price_range.quantity_to4 = update_form.quantity_to4.data
        price_range.unit_price4 = update_form.unit_price4.data
        price_range.imprinting_prices4 = update_form.imprinting_prices4.data
        price_range.setup_cost4 = update_form.setup_cost4.data
        price_range.freight_cost4 = update_form.freight_cost4.data

        price_range.quantity_from5 = update_form.quantity_from5.data
        price_range.quantity_to5 = update_form.quantity_to5.data
        price_range.unit_price5 = update_form.unit_price5.data
        price_range.imprinting_prices5 = update_form.imprinting_prices5.data
        price_range.setup_cost5 = update_form.setup_cost5.data
        price_range.freight_cost5 = update_form.freight_cost5.data

        #map prod and price_range
        prod.price_ranges = [price_range]

        #map prod and picture
        prod.prod_pics=[]

        #Pictures

        # cover_img_file = request.files['cover_img_file']
        # if  cover_img_file.filename :
        #     if allowed_file(cover_img_file.filename):
        #             filename = "{prod_name}{time}.{ext}".format( prod_name=prod.prod_name ,
        #                                                          time=datetime.datetime.now().isoformat().replace(':','_').replace('.','_') ,
        #                                                          ext=secure_filename(cover_img_file.filename)[-3:])
        #             prod.cover_img = filename #os.path.join(PROD_UPLOAD_PATH, filename)
        #             cover_img_file.save(os.path.join(PROD_UPLOAD_PATH, filename))
        #     else :
        #             flash("Only accept {types} file".format(types=ALLOWED_EXTENSIONS),category='danger')
        #             prod.cover_img = this_prod.cover_img
        # else:
        #     prod.cover_img = this_prod.cover_img

        cover_img_file = request.files['cover_img_file']
        filename = saveImage(cover_img_file,prod)
        prod.cover_img = filename if filename else this_prod.cover_img

        #append new extra file list
        extra_imgs = request.files.getlist('extra_img_file')
        extra_descs =request.form.getlist('extra_img_desc')
        for i in range(extra_imgs.__len__()):
            e_i_picture = Prod_pic_info()
            # e_i_filename = "{prod_name}{time}.{ext}".format( prod_name=prod.prod_name ,
            #                                                  time=datetime.datetime.now().isoformat().replace(':','_').replace('.','_'),
            #                                                  ext=secure_filename(extra_imgs[i].filename)[-3:])
            # e_i_picture.image_path = e_i_filename    #os.path.join(PROD_UPLOAD_PATH, e_i_filename)
            # extra_imgs[i].save(os.path.join(PROD_UPLOAD_PATH, e_i_filename))
            #
            # e_i_picture.img_desc = extra_descs[i]
            # e_i_picture.valid_flg = 1
            # prod.prod_pics.append(e_i_picture)

            e_i_filename = saveImage(extra_imgs[i],prod)
            if e_i_filename:
                e_i_picture.image_path = e_i_filename
                e_i_picture.img_desc = extra_descs[i]
                e_i_picture.valid_flg = 1
                prod.prod_pics.append(e_i_picture)

        #append existing extra file list
        for p in this_prod.prod_pics:
            existing_extra_pic = Prod_pic_info()
            existing_extra_pic.img_desc=p.img_desc
            existing_extra_pic.image_path=p.image_path
            existing_extra_pic.valid_flg=1
            prod.prod_pics.append(existing_extra_pic)


        #s = Session()
        prod.supplier_id = current_user.supplier_id
        s.commit()
        s.query(Prod_info).filter_by(prod_id=this_prod.prod_id).delete()
        s.flush()
        s.merge(prod)
        message = "Update production {name} successfully!".format(name=prod.prod_name)
        s.commit()
        flash(message,category='info')
        return redirect(url_for('supplierRoute.update_prod',prod_id=prod.prod_id))
    elif request.method == 'POST':
        this_prod = None
        flash(update_form.errors, category='danger')
        return redirect(url_for("supplierRoute.index"))
    else:
        prod_id = request.args.get('prod_id', 1) if request.method == 'GET' else request.form.get('prod_id', 1)
        print(prod_id)
        this_prod = s.query(Prod_info).filter_by(prod_id=prod_id).first()
        this_prod.price_ranges = this_prod.price_ranges if this_prod.price_ranges.__len__()>0 else [Prod_price_range()]

    return render_template("admin_temp/update_prod_form.html",
                           update_form=update_form,
                           this_prod=this_prod)


@supplierRoute.route("/delete_prod",methods=['GET','POST'])
@login_required
def delete_prod():
    prod_id = request.form.get('prod_id')
    print(prod_id)
    if prod_id:
        s = Session()
        s.query(Prod_info).filter_by(prod_id=prod_id).delete()
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for delete production',category='danger')
        return jsonify(result='failed')


@supplierRoute.route("/delete_cover_page",methods=['GET','POST'])
@login_required
def delete_cover_page():
    prod_id = request.form.get('prod_id')
    if prod_id:
        s = Session()
        s.query(Prod_info).filter_by(prod_id=prod_id).update({
            'cover_img' : 'default.png'
        })
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for delete coverage image',category='danger')
        return '<HTML><h2>No Valid information for delete coverage image</h2></HTML>'


@supplierRoute.route("/delete_extra_pics",methods=['GET','POST'])
@login_required
def delete_extra_pics():
    prod_pic_id = request.form.get('prod_pic_id')
    if prod_pic_id:
        s = Session()
        s.query(Prod_pic_info).filter_by(prod_pic_id=prod_pic_id).delete()
        s.commit()
        s.close()
        return jsonify(result='succ')
    else:
        flash('No Valid information for delete coverage image',category='danger')
        return '<HTML><h2>No Valid information for delete coverage image</h2></HTML>'
