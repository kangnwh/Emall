# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request,redirect,render_template,url_for,abort,jsonify
from flask_login import login_required,current_user

from webapp.Models.db_basic import Session
from webapp.Models.prod_info import Prod_info
from webapp.Models.v_prod_price_range import V_Prod_price_range
from webapp.Models.order_system import Order_system
from webapp.Models.quote_system import Quote_system
from webapp.Models.compliment_system import Compliment_system
from webapp.viewrouting.order.forms.order_forms import UserOrderForm,UserQuoteForm

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

@orderRoute.route("/user_cancel",methods=["GET"])
@login_required
def user_cancel():
    s = Session()
    client_order_id = request.args.get('client_order_id', -1)
    this_order = s.query(Order_system).filter_by(client_order_id=client_order_id)
    if this_order.first().order_stat == 1 or current_user.is_administrator:
        this_order.update({
            "order_stat":6
        })
        s.commit()
        return redirect(url_for("adminRoute.all_orders",type='canceled')) if current_user.is_administrator else redirect(url_for("userRoute.user_orders",type='canceled')), s.close()
    else:
        flash("Cannot cancel this order in this phase.","warning")
        return redirect(url_for("userRoute.user_orders",type='ongoing')), s.close()



@orderRoute.route("/show_one_order", methods=["GET", "POST"])
@login_required
def show_one_order():
    s = Session()
    client_order_id = request.args.get('client_order_id', -1)
    this_order = s.query(Order_system).filter_by(client_order_id=client_order_id).first()
    # s.close()
    return render_template('order_temp/show_one_order.html',
                           this_order=this_order), s.close()

@orderRoute.route("/user_feedback",methods=["POST"])
@login_required
def user_feedback():
    s = Session()

    client_order_id = request.form.get('client_order_id')
    content = request.form.get('content','')

    this_order = s.query(Order_system).filter_by(client_order_id=client_order_id)

    feedback = Compliment_system()

    feedback.user_id = current_user.user_id
    feedback.prod_id = this_order.first().prod_id
    feedback.order_id = this_order.first().order_id
    feedback.compliment_rate = request.form.get('rating',0)
    feedback.user_compliment_comments = content

    if this_order.first().order_stat == 3 :
        this_order.update({
            "order_stat":5
            # 'user_comments':this_order.first().user_comments +content
        })
        s.add(feedback)
        s.commit()
        return jsonify(result='succ') #redirect(url_for("adminRoute.user_orders",type='finished')) if current_user.is_administrator else redirect(url_for("userRoute.user_orders",type='finished')), s.close()
    else:
        flash("Cannot provide feedback to this order in this phase.","warning")
        return jsonify(result='failed')#return redirect(url_for("userRoute.user_orders",type='ongoing')), s.close()


@orderRoute.route("/create_quote",methods=["GET","POST"])
@login_required
def create_quote():
    user_quote_form = UserQuoteForm()
    if user_quote_form.validate_on_submit():
        quote = Quote_system()
        quote.user_id = current_user.user_id
        quote.quote_name=user_quote_form.quote_name.data
        quote.supplier_id = user_quote_form.supplier_id.data
        quote.prod_id = user_quote_form.prod_id.data
        quote.prod_name = user_quote_form.prod_name.data
        quote.prod_quantity = user_quote_form.prod_quantity.data
        quote.imprint_info = user_quote_form.imprint_info.data
        quote.special_instruction = user_quote_form.special_instruction.data
        quote.colors = user_quote_form.colors.data
        quote.lead_time = user_quote_form.lead_time.data

        quote.user_perfer_unit_price = user_quote_form.user_perfer_unit_price.data
        quote.user_perfer_imprinting_prices = user_quote_form.user_perfer_imprinting_prices.data
        quote.user_perfer_setup_cost = user_quote_form.user_perfer_setup_cost.data
        quote.user_perfer_freight_cost = user_quote_form.user_perfer_freight_cost.data
        quote.user_perfer_total = quote.user_perfer_unit_price * quote.prod_quantity + quote.user_perfer_imprinting_prices + quote.user_perfer_setup_cost + quote.user_perfer_freight_cost #user_quote_form.user_perfer_total.data

        quote.user_perfer_comment = user_quote_form.user_perfer_comment.data
        quote.is_return_flg = 0
        quote.valid_flg = 1

        s = Session()
        s.add(quote)
        s.commit()
        s.close()

        flash("Quote Submitted","success")
        return redirect(url_for("userRoute.user_quotes",type='ongoing'))#render_template("reload_parent.html")#reload_parent.html
    elif request.method == 'POST':
        flash(user_quote_form.errors, category='danger')
        return redirect(url_for("orderRoute.create_quote",prod_id=user_quote_form.prod_id.data))
    else:
        s = Session()
        prod_id = request.args.get('prod_id', 1)
        this_prod = s.query(Prod_info).filter_by(prod_id=prod_id).first()
        return render_template("order_temp/quote.html",
                               this_prod=this_prod,
                               user_quote_form = user_quote_form) , s.close()


@orderRoute.route("/show_one_quote", methods=["GET", "POST"])
@login_required
def show_one_quote():
    s = Session()
    quote_id = request.args.get('quote_id', -1)
    this_quote = s.query(Quote_system).filter_by(quote_id=quote_id).first()
    # s.close()
    return render_template('order_temp/show_one_quote.html',
                           this_quote=this_quote), s.close()
