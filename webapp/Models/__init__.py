from webapp.Models.db_basic import engine,Session,Base
# from webapp.Models.user import User
# from webapp.Models.tag import Tag
# from webapp.Models.item import Item
# from webapp.Models.map_user_tag import Map_User_Tag
# from webapp.Models.map_tag_item import Map_Tag_Item
from webapp.Models.order_system import Order_system
from webapp.Models.quote_system import Quote_system
from webapp.Models.prod_info import Prod_info
from webapp.Models.supplier_rebate_ref import Supplier_rebate_ref
from flask_login import login_required,current_user
from sqlalchemy import func,between,and_


def get_pending_order_count(type,id):
    s = Session()
    base_query = s.query(func.count(Order_system.order_id)).filter(Order_system.order_stat.between(1,3))
    if type == 'user':
        count = base_query.filter(Order_system.user_id==id).first()[0]
    elif type == 'supplier':
        count = base_query.filter(Order_system.supplier_id==id).first()[0]
    else:
        count = None
    s.close()
    return count


def get_pending_quote_count(type,id):
    s = Session()
    base_query = s.query(func.count(Quote_system.quote_id)).filter(Quote_system.is_return_flg==0)
    if type == 'user':
        count = base_query.filter(Quote_system.user_id==id).first()[0]
    elif type == 'supplier':
        count = base_query.filter(Quote_system.supplier_id==id).first()[0]
    else:
        count = None
    s.close()
    return count

def get_supplier_level(type,id):
    s = Session()
    supplier_rebate_ref=s.query(Supplier_rebate_ref).filter(between(current_user.supplier_points,Supplier_rebate_ref.supplier_points_from,Supplier_rebate_ref.supplier_points_to)).first()
    if type == 'supplier':
        count = supplier_rebate_ref.supplier_level
    else:
        count = None
    s.close()
    return count

def get_approval_pending_count(type,id):
    s = Session()
    base_query = s.query(func.count(Prod_info.prod_id)).filter(and_(Prod_info.approve_stat.in_([0,-1]),Prod_info.is_del_flg==0))
    if type == 'user':
        count = base_query.filter(Prod_info.approve_stat==0).first()[0]
    elif type == 'supplier':
        count = base_query.filter(Prod_info.supplier_id==id).first()[0]
    else:
        count = None
    s.close()
    return count
