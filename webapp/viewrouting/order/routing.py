# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request,redirect,render_template,url_for
from flask_login import login_required,current_user

from webapp.Models.db_basic import Session
from webapp.Models.prod_info import Prod_info
from webapp.Models.v_prod_price_range import V_Prod_price_range
from webapp.Models.order_system import Order_system
from webapp.viewrouting.order.forms.order_forms import UserOrderForm

import datetime

orderRoute = Blueprint('orderRoute', __name__,
                      template_folder='templates', static_folder='static')


@orderRoute.route("/create_order",methods=["GET","POST"])
@login_required
def create_order():
    user_order_form = UserOrderForm()
    if user_order_form.validate_on_submit():
        order = Order_system()
        order.user_id = current_user.user_id
        order.client_order_id = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")#int("{userid}{timeflag}".format(userid=current_user.user_id,timeflag=timeflag))
        order.supplier_id = user_order_form.supplier_id.data
        order.prod_id = user_order_form.prod_id.data
        order.prod_name = user_order_form.prod_name.data
        order.prod_quantity = user_order_form.prod_quantity.data
        order.imprint_info = user_order_form.imprint_info.data
        order.colors = user_order_form.colors.data
        order.lead_time = user_order_form.lead_time.data
        order.unit_price = user_order_form.unit_price.data
        order.imprinting_prices = user_order_form.imprinting_prices.data
        order.setup_cost = user_order_form.setup_cost.data
        order.freight_cost = user_order_form.freight_cost.data
        order.total_price = user_order_form.total_price.data

        order.need_pay_supplier = 0 #TODO need complex logic to get this value
        order.is_used_points = False
        order.used_points = False
        order.user_comments = user_order_form.user_comments.data
        order.order_stat = 1 # stands for user submitting
        order.valid_flg = 1

        s = Session()
        s.add(order)
        s.commit()
        s.close()

        flash("Order Submitted","success")
        return render_template("reload_parent.html")#reload_parent.html
    elif request.method == 'POST':
        flash(user_order_form.errors, category='danger')
        return redirect(url_for("orderRoute.create_order",prod_id=request.args.get('prod_id', 1)))
    else:
        s = Session()
        prod_id = request.args.get('prod_id', 1)
        this_prod = s.query(Prod_info).filter_by(prod_id=prod_id).first()
        return render_template("order_temp/buy.html",
                               this_prod=this_prod,
                               user_order_form = user_order_form) , s.close()

@orderRoute.route("/user_orders/<type>",methods=["GET"])
@login_required
def user_orders(type):
    s = Session()
    if type == 'finished':
        order_list = s.query(Order_system).filter(order_stat)
    elif type=='ongoing':
        pass
    else:
        pass
