# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request,redirect,render_template,url_for,abort,jsonify
from flask_login import login_required,current_user
from sqlalchemy import func,or_,and_,between,INTEGER,DECIMAL
from webapp.Models.db_basic import Session
from webapp.Models.prod_info import Prod_info
from webapp.Models.v_prod_price_range import V_Prod_price_range
from webapp.Models.prod_price_range import Prod_price_range
from webapp.Models.order_system import Order_system
from webapp.Models.quote_system import Quote_system
from webapp.Models.supplier_rebate_ref import Supplier_rebate_ref
from webapp.Models.user import User
from webapp.Models.supplier import Supplier
from webapp.Models.compliment_system import Compliment_system
from webapp.viewrouting.order.forms.order_forms import UserOrderForm,UserQuoteForm,QuoteToOrderForm
from webapp.common.mails import send_email_base,email_notifier
import datetime
import decimal
import webapp.config.customer_config as customer_config

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
        order.prod_size=user_order_form.prod_size.data
        order.special_instruction=user_order_form.special_instruction.data

        s = Session()
        this_prod = s.query(Prod_info).filter_by(prod_id=order.prod_id,is_del_flg=0,valid_flg=1).first()
        if not this_prod:
            flash("Invalid production!","warning")
            return redirect(url_for('homeRoute.index'))
        this_supplier=s.query(Supplier).filter_by(supplier_id=order.supplier_id).first()
        supplier_rebate_ref=s.query(Supplier_rebate_ref).filter(between(this_supplier.supplier_points,Supplier_rebate_ref.supplier_points_from,Supplier_rebate_ref.supplier_points_to)).first()
        supplier_rebate_rate=supplier_rebate_ref.rebate_rate
        # print(supplier_rebate_rate)
        if this_prod.is_special_price_flg ==1 :
            order.unit_price = this_prod.special_price_new
            real_unit_price = this_prod.special_price_new
            order.total_price = this_prod.special_price_new * order.prod_quantity
            order.imprinting_prices,order.setup_cost,order.freight_cost = [0]*3
        else:
            prices = s.query(V_Prod_price_range).filter_by(prod_id=order.prod_id).first()
            order.total_price,order.unit_price,order.imprinting_prices,order.setup_cost,order.freight_cost = prices.get_prices(order.prod_quantity)
            real_prices = s.query(Prod_price_range).filter_by(prod_id=order.prod_id).first()
            real_unit_price=real_prices.get_unit_prices(order.prod_quantity)
        tmp_used_pts=0
        if user_order_form.is_used_points.data ==1 :
            order.is_used_points = 1
            order.used_points = user_order_form.used_points.data
            if user_order_form.used_points.data >= current_user.credit_points :
                tmp_used_pts=current_user.credit_points
            else:
                tmp_used_pts=user_order_form.used_points.data
            order.pts_deduct = (tmp_used_pts * decimal.Decimal(customer_config.USER_POINT_DISCOUNT_RATE)) / 100
            tmp_total_price=order.total_price
            order.total_price=decimal.Decimal(tmp_total_price) - decimal.Decimal(order.pts_deduct)
        else:
            order.is_used_points = 0
            order.used_points = 0
            order.pts_deduct = 0
        order.need_pay_supplier = (real_unit_price * (1 + supplier_rebate_rate/100)) * order.prod_quantity  + order.imprinting_prices + order.setup_cost + order.freight_cost
        order.user_comments = user_order_form.user_comments.data
        order.order_stat = 1 # stands for user submitting
        order.valid_flg = 1

        new_credit_points=current_user.credit_points - tmp_used_pts
        user_id = current_user.user_id
        s.query(User).filter_by(user_id=user_id).update(
                {
                    "credit_points": new_credit_points
                }
        )

        s.add(order)
        s.commit()
        email_notifier([order.supplier.email], "New Order Created", order.notification_to_supplier())

        s.close()
        #send notification via email

        # send_email_base("New Order Coming", ['recipients'], '', 'html_body')
        flash("Order Submitted","success")
        return redirect(url_for("userRoute.user_orders",type='ongoing'))#render_template("reload_parent.html")#reload_parent.html
    elif request.method == 'POST':
        flash(user_order_form.errors, category='danger')
        return redirect(url_for("orderRoute.create_order",prod_id=user_order_form.prod_id.data))
    else:
        s = Session()
        prod_id = request.args.get('prod_id', 1)
        this_prod = s.query(Prod_info).filter_by(prod_id=prod_id).first()
        if this_prod.is_special_price_flg == 1:
            return render_template("order_temp/buy_special_price.html",
                                   this_prod=this_prod,
                                   user_order_form = user_order_form) , s.close()
        else:
            return render_template("order_temp/buy.html",
                                   this_prod=this_prod,
                                   user_order_form = user_order_form) , s.close()

@orderRoute.route("/user_cancel",methods=["GET"])
@login_required
def user_cancel():
    s = Session()
    client_order_id = request.args.get('client_order_id', -1)
    this_order_query = s.query(Order_system).filter_by(client_order_id=client_order_id)
    this_order = this_order_query.first()
    if this_order.order_stat == 1 or current_user.is_administrator:
        this_order_query.update({
            "order_stat":6
        })
        if this_order.is_used_points == 1 and this_order.used_points != 0 :
            user_id = this_order.user_id
            this_user_query=s.query(User).filter_by(user_id=user_id).first()
            this_user = this_user_query.first()
            curr_tmp_pts=this_user.credit_points
            new_tmp_pts=curr_tmp_pts+this_order.used_points
            this_user_query.update(
                {
                    "credit_points": new_tmp_pts
                }
            )
        s.commit()
        email_notifier([this_order.supplier.email], "Order Canceled By User", this_order.notification_to_supplier())
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
        after_order = s.query(Order_system).filter_by(client_order_id=client_order_id)
        if this_order.first().order_stat == 5 :
            new_pts=after_order.first().total_price
            after_user = s.query(User).filter_by(user_id=current_user.user_id)
            new_user_pts=current_user.credit_points + round(new_pts/100)
            after_user.update({
                "credit_points" : new_user_pts
            })
            after_supplier=s.query(Supplier).filter_by(supplier_id=this_order.first().supplier_id)
            current_supplier_pts=after_supplier.first().supplier_points
            new_supplier_pts=current_supplier_pts+round(new_pts/100)
            after_supplier.update({
                "supplier_points" : new_supplier_pts
            })

            # print(new_pts)
            # print(new_user_pts)
            # print(new_supplier_pts)

            s.commit()

            email_notifier([this_order.supplier.email], "Order Finished", this_order.notification_to_supplier())
            s.close()
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
        quote.prod_size=user_quote_form.prod_size.data

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
        email_notifier([quote.supplier.email], "New Quote Created", quote.notification_to_supplier())
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

@orderRoute.route("/quote_to_order",methods=["GET","POST"])
@login_required
def quote_to_order():
    s = Session()
    quote_to_order_form=QuoteToOrderForm()
    if quote_to_order_form.validate_on_submit():
        new_quote = s.query(Quote_system).filter_by(quote_id=quote_to_order_form.quote_id.data).first()
        order = Order_system()
        order.user_id = current_user.user_id
        order.client_order_id = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")#int("{userid}{timeflag}".format(userid=current_user.user_id,timeflag=timeflag))
        order.supplier_id = new_quote.supplier_id
        order.prod_id = new_quote.prod_id
        order.prod_name = new_quote.prod_name
        order.prod_quantity = new_quote.prod_quantity
        order.imprint_info = new_quote.imprint_info
        order.colors = new_quote.colors
        order.lead_time = new_quote.lead_time
        order.prod_size=new_quote.prod_size
        order.special_instruction=new_quote.special_instruction

        order.total_price=new_quote.supplier_perfer_total
        order.unit_price=new_quote.supplier_perfer_unit_price
        order.imprinting_prices=new_quote.supplier_perfer_imprinting_prices
        order.setup_cost=new_quote.supplier_perfer_setup_cost
        order.freight_cost=new_quote.supplier_perfer_freight_cost

        this_supplier=s.query(Supplier).filter_by(supplier_id=order.supplier_id).first()
        supplier_rebate_ref=s.query(Supplier_rebate_ref).filter(between(this_supplier.supplier_points,Supplier_rebate_ref.supplier_points_from,Supplier_rebate_ref.supplier_points_to)).first()
        supplier_rebate_rate=supplier_rebate_ref.rebate_rate
        print(supplier_rebate_rate)

        real_prices = s.query(Prod_price_range).filter_by(prod_id=order.prod_id).first()
        real_unit_price=real_prices.get_unit_prices(order.prod_quantity)
        order.need_pay_supplier = (real_unit_price * (1 + supplier_rebate_rate/100)) * order.prod_quantity  + order.imprinting_prices + order.setup_cost + order.freight_cost
        order.is_used_points = 0
        order.used_points = 0
        order.pts_deduct = 0
        order.user_comments = quote_to_order_form.user_comments.data
        order.order_stat = 1 # stands for user submitting
        order.valid_flg = 1
        order.sys_quote_id=quote_to_order_form.quote_id.data


        s.add(order)
        s.commit()
        s.close()

        quote_id=quote_to_order_form.quote_id.data
        flash("Order Submitted","success")
    elif request.method == 'POST':
        flash(quote_to_order_form.errors, category='danger')
        quote_id = quote_to_order_form.quote_id.data
    else:
        quote_id = request.args.get('quote_id')
        if not quote_id:
            flash("Request invalid", "warning")
            return redirect(url_for("userRoute.user_quotes", type="finish"))

    this_quote = s.query(Quote_system).filter_by(quote_id=quote_id).first()
    return render_template("order_temp/quote_to_order.html",
                           this_quote=this_quote,
                           quote_to_order_form=quote_to_order_form), s.close()