 # -*- coding: utf-8 -*-
from flask import Blueprint,request,redirect,url_for
from flask_login import login_required,current_user,logout_user
from webapp.viewrouting.admin.real_routing import _index,_account_management,_prod_cate_mgt,_spec_links,_delete_user,_add_user,_update_user,\
                                                    _add_level_one,_delete_level_one,_update_level_one,_all_orders,_all_quotes,\
                                                    _delete_level_two,_update_level_two,_add_level_two,_reset_password,\
                                                    _manage_supplier_rebate_rate,_delete_rebate,_update_rebate,_add_rebate,\
                                                    _manage_profit_rate,_delete_profit,_add_profit,_update_profit,_supplier_management,_update_supplier,_reset_supp_passwd
                                                    #_publish_prod, _add_new_prod,_update_prod,_delete_prod,_delete_cover_page,_delete_extra_pics,
adminRoute = Blueprint('adminRoute', __name__,
                      template_folder='templates', static_folder='static')




@adminRoute.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return _index()


@adminRoute.route('/actmgt', methods=['GET', 'POST'])
@login_required
def account_management():
    return _account_management()

@adminRoute.route('/supplier_management', methods=['GET', 'POST'])
@login_required
def supplier_management():
    return _supplier_management()

@adminRoute.route('/prod_cate_mgt', methods=['GET', 'POST'])
@login_required
def prod_cate_mgt():
    return _prod_cate_mgt()

# @adminRoute.route('/publish_prod', methods=['GET', 'POST'])
# @login_required
# def publish_prod():
#     return _publish_prod()


@adminRoute.route('/spec_links', methods=['GET'])
@login_required
def spec_links():
   return _spec_links()


@adminRoute.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    return _delete_user()

@adminRoute.route('/add_user', methods=['POST'])
@login_required
def add_user():
    return _add_user()

@adminRoute.route('/update_user', methods=['POST'])
@login_required
def update_user():
    return _update_user()

@adminRoute.route('/update_supplier', methods=['POST'])
@login_required
def update_supplier():
    return _update_supplier()

@adminRoute.route('/add_level_one', methods=['POST'])
@login_required
def add_level_one():
    return _add_level_one()


@adminRoute.route('/delete_level_one', methods=['POST'])
@login_required
def delete_level_one():
    return _delete_level_one()

@adminRoute.route('/update_level_one', methods=['POST'])
@login_required
def update_level_one():
    return _update_level_one()

@adminRoute.route('/add_level_two', methods=['POST'])
@login_required
def add_level_two():
    return _add_level_two()


@adminRoute.route('/delete_level_two', methods=['POST'])
@login_required
def delete_level_two():
    return _delete_level_two()

@adminRoute.route('/update_level_two', methods=['POST'])
@login_required
def update_level_two():
    return _update_level_two()


@adminRoute.route('/reset_password', methods=['POST'])
@login_required
def reset_password():
    return _reset_password()

@adminRoute.route('/reset_supp_passwd', methods=['POST'])
@login_required
def reset_supp_passwd():
    return _reset_supp_passwd()
#
# @adminRoute.route('/add_new_prod', methods=['GET','POST'])
# @login_required
# def add_new_prod():
#     return _add_new_prod()
#
# @adminRoute.route('/update_prod', methods=['GET','POST'])
# @login_required
# def update_prod():
#     return _update_prod()
#
# @adminRoute.route('/delete_prod', methods=['POST'])
# @login_required
# def delete_prod():
#     return _delete_prod()
#
# @adminRoute.route('/delete_cover_page', methods=['POST'])
# @login_required
# def delete_cover_page():
#     return _delete_cover_page()
#
# @adminRoute.route('/delete_extra_pics', methods=['POST'])
# @login_required
# def delete_extra_pics():
#     return _delete_extra_pics()


@adminRoute.route('/manage_profit_rate', methods=['GET', 'POST'])
@login_required
def manage_profit_rate():
    return _manage_profit_rate()

@adminRoute.route('/delete_profit', methods=['POST'])
@login_required
def delete_profit():
    return _delete_profit()

@adminRoute.route('/add_profit', methods=['POST'])
@login_required
def add_profit():
    return _add_profit()

@adminRoute.route('/update_profit', methods=['POST'])
@login_required
def update_profit():
    return _update_profit()

@adminRoute.route('/manage_supplier_rebate_rate', methods=['GET', 'POST'])
@login_required
def manage_supplier_rebate_rate():
    return _manage_supplier_rebate_rate()

@adminRoute.route('/delete_rebate', methods=['POST'])
@login_required
def delete_rebate():
    return _delete_rebate()

@adminRoute.route('/add_rebate', methods=['POST'])
@login_required
def add_rebate():
    return _add_rebate()

@adminRoute.route('/update_rebate', methods=['POST'])
@login_required
def update_rebate():
    return _update_rebate()

@adminRoute.route("/all_orders/<type>",methods=["GET"])
@login_required
def all_orders(type):
    return _all_orders(type)

@adminRoute.route("/all_quotes/<type>",methods=["GET"])
@login_required
def all_quotes(type):
    return _all_quotes(type)

@adminRoute.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('homeRoute.index'))