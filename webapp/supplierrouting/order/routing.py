# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request,redirect,render_template,url_for,abort
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


        s = Session()
        prices = s.query(V_Prod_price_range).filter_by(prod_id=order.prod_id).first()
        order.total_price,order.unit_price,order.imprinting_prices,order.setup_cost,order.freight_cost = prices.get_prices(order.prod_quantity)

        order.need_pay_supplier = 0 #TODO need complex logic to get this value
        order.is_used_points = 1 if order.is_used_points else 0
        order.used_points = order.used_points
        order.user_comments = user_order_form.user_comments.data
        order.order_stat = 1 # stands for user submitting
        order.valid_flg = 1


        s.add(order)
        s.commit()
        s.close()

        flash("Order Submitted","success")
        return redirect(url_for("userRoute.user_orders",type='ongoing'))#render_template("reload_parent.html")#reload_parent.html
    elif request.method == 'POST':
        flash(user_order_form.errors, category='danger')
        return redirect(url_for("orderRoute.create_order",prod_id=user_order_form.prod_id.data))
    else:
        s = Session()
        prod_id = request.args.get('prod_id', 1)
        this_prod = s.query(Prod_info).filter_by(prod_id=prod_id).first()
        return render_template("order_temp/buy.html",
                               this_prod=this_prod,
                               user_order_form = user_order_form) , s.close()



@orderRoute.route("/show_one_order", methods=["GET", "POST"])
@login_required
def show_one_order():
    s = Session()
    client_order_id = request.args.get('client_order_id', -1)
    this_order = s.query(Order_system).filter_by(client_order_id=client_order_id).first()
    if this_order:
        return render_template('order_temp/show_one_order.html',
                           this_order=this_order), s.close()
    else:
        flash("No order found with client_order_id:{id}".format(client_order_id),"warning")
        return render_template("reload_parent.html")
    # s.close()


@orderRoute.route("/receive",methods=["GET"])
@login_required
def receive_order():
    s = Session()
    client_order_id = request.args.get('client_order_id', -1)
    request_from = request.args.get('order_list', None)
    this_order = s.query(Order_system).filter_by(client_order_id=client_order_id)
    if this_order.first().order_stat == 1:
        this_order.update({
            "order_stat":2
        })
        s.commit()
        flash("You received order {id}, please deliver as soon as possible.".format(id=client_order_id),"success")
        return redirect(url_for("userRoute.user_orders",type='ongoing')) if request_from else render_template("reload_parent.html") , s.close()
    else:
        flash("Cannot receive this order in this phase.","warning")
        return redirect(url_for("orderRoute.show_one_order",client_order_id=request.args.get('client_order_id', -1))), s.close()

@orderRoute.route("/deliver",methods=["GET"])
@login_required
def deliver():
    s = Session()
    client_order_id = request.args.get('client_order_id', -1)
    request_from = request.args.get('order_list', None)
    this_order = s.query(Order_system).filter_by(client_order_id=client_order_id)
    if this_order.first().order_stat == 2:
        this_order.update({
            "order_stat":3
        })
        s.commit()
        flash("Order is now in delivering phase.".format(id=client_order_id),"success")
        return redirect(url_for("userRoute.user_orders",type='ongoing')) if request_from else render_template("reload_parent.html") , s.close()
    else:
        flash("Cannot deliver this order in this phase.","warning")
        return redirect(url_for("orderRoute.show_one_order",client_order_id=request.args.get('client_order_id', -1))), s.close()