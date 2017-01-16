import datetime
import hashlib
import os
import random


from PIL import Image
from flask import flash, redirect, url_for,current_app
from flask_login import current_user
from flask_paginate import Pagination
from sqlalchemy import or_
from werkzeug import secure_filename

from webapp.Models.db_basic import Session
from webapp.Models.prod_cat import Prod_cat
from webapp.Models.prod_info import Prod_info
from webapp.Models.order_system import Order_system
from webapp.Models.quote_system import Quote_system
from webapp.Models.supplier import Supplier
from webapp.Models.prod_sub_cat import Prod_sub_cat

from webapp.config.config import HOST_INFO



def generate_security_key(key_len):
    pwdStrPool = '0123456789' \
                 'abcdefghijkmnpqrstuvwxyz' \
                 '~@#$%^&*()_+|' \
                 'ABCDEFGHIJKMNPQRSTUVWXYZ'
    array_len = len(pwdStrPool)
    security_key = [pwdStrPool[i] for i in (random.randint(0, array_len - 1) for x in range(key_len))]
    return ''.join(security_key)


def generate_md5(data):
    md5 = hashlib.md5(data.encode('ascii'))
    return md5.hexdigest()


def update_config_value(parameter,value):
    new_pair = {parameter:value}
    current_app.config.update(new_pair)

    import webapp as w
    import shutil
    config_folder = os.path.dirname(w.__file__)
    customer_config = config_folder + os.sep + 'config' + os.sep + 'customer_config.py'
    customer_config_temp = customer_config+".temp"
    with open(customer_config, 'r') as f:
        with open(customer_config_temp, 'w') as g:
            for line in f.readlines():
                if parameter not in line:
                    g.write(line)
                else:
                    g.write('{parameter}={value}{breaker}'.format(parameter=parameter,value=value,breaker=os.linesep))
    shutil.move(customer_config_temp, customer_config)


def generate_sidebar():
    first_level_list = list()
    first_level_list.append(
        '<aside ><section  class="sidebar">	    <ul class="sidebar-menu">	      <li class="header">Navigation</li>')
    first_level_list.append('''<li class="treeview">
    <a href="{{ url_for("homeRoute.hot_prods") }}">
         <i class="fa fa-dashboard"></i>
         <span class='strong-title'>Hot Productions</span>
         <i class="fa fa-angle-left pull-right"></i>
     </a>
        ''')
    first_level_list.append('''<li class="treeview">
    <a href="{{ url_for("homeRoute.clearance") }}">
         <i class="fa fa-dashboard"></i>
         <span class='strong-title'>Clearance</span>
         <i class="fa fa-angle-left pull-right"></i>
     </a>
        ''')
    first_level_list.append('''<li class="treeview">
    <a href="{{ url_for("homeRoute.on_sale") }}">
         <i class="fa fa-dashboard"></i>
         <span class='strong-title'>On Sale</span>
         <i class="fa fa-angle-left pull-right"></i>
     </a>
        ''')
    s = Session()
    category_list = s.query(Prod_cat).filter_by(valid_flg=1).order_by(Prod_cat.prod_cat_order)

    for first_level in category_list:
        first_level_list.append('''
        <li class="treeview {{% if {prod_cat_id}== nav_active %}}active{{% endif %}}"><a href="#"> <i class="fa fa-dashboard"></i> <span>{cat_name}</span> <i class="fa fa-angle-left pull-right"></i></a>
        '''.format(prod_cat_id=first_level.prod_cat_id, cat_name=first_level.prod_cat_name))

        first_level_list.append('<ul class="treeview-menu">')

        for second_level in first_level.prod_sub_cat:
            first_level_list.append(
                '<li><a href="{{ url_for("homeRoute.sub_category_list",sub_cat_id=%s) }}"><i class="fa fa-circle-o"></i>%s</a></li>' % (
                second_level.prod_cat_sub_id, second_level.prod_cat_sub_name))

        first_level_list.append('</ul></li>')

    first_level_list.append('</ul></section></aside>')

    content = ''.join(first_level_list)

    import webapp as w
    sidebar_template_folder = os.path.dirname(w.__file__)
    sidebar_template = sidebar_template_folder + os.sep + 'templates' + os.sep + 'sidebar.html'
    with open(sidebar_template, 'w') as f:
        f.write(content)

    return content


def admin_check(func):
    def real_func(*args, **kwargs):
        if current_user.is_administrator:
            ret = func(*args, **kwargs)
            return ret
        else:
            flash("You are not an administrator for this system, please use an admin id.", category='danger')
            return redirect(url_for("userRoute.login"))

    return real_func


def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1] in current_app.config.get("ALLOWED_EXTENSIONS"):
        return True
    else:
        return False


def saveImage(request_file, prod):
    if request_file.filename:
        if allowed_file(request_file.filename):
            filename = "{prod_name}{time}.{ext}".format(prod_name=prod.prod_name,
                                                        time=datetime.datetime.now().isoformat().replace(':',
                                                                                                         '_').replace(
                                                            '.', '_'),
                                                        ext=secure_filename(request_file.filename)[-3:])
            request_file.save(os.path.join(current_app.config.get("PROD_UPLOAD_PATH"), filename))
            return filename
        else:
            flash("Only accept {types} file".format(types=current_app.config.get("ALLOWED_EXTENSIONS")), category='danger')

    return False


def generatePNG(image):
    img = Image.open(current_app.config.get("USER_LOGO_UPLOAD_PATH") + image)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] >= 220 and item[1] >= 220 and item[2] >= 220:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(current_app.config.get("USER_LOGO_UPLOAD_PATH") + 'GEN_' + image, "PNG")


def object2dict(obj):
    # convert object to a dict
    d = {}
    # d['__class__'] = obj.__class__.__name__
    # d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d


def get_host_info(type):
    ip = HOST_INFO[type]['IP']
    port = HOST_INFO[type]['PORT']
    return ip,port


def prod_search_filter(keyword,query_base,page,supplier_id=None):
    if keyword and query_base:
        w = "%{keyword}%".format(keyword=keyword)
        s = Session()
        prod_list_query = query_base.filter(Prod_info.supplier_id == Supplier.supplier_id)\
                                    .filter(Prod_info.prod_cat_sub_id == Prod_sub_cat.prod_cat_sub_id)\
                                        .filter(or_(Supplier.supplier_name.like(w),
                                                Prod_info.prod_name.like(w),
                                                Prod_info.prod_id.like(w),
                                                Prod_sub_cat.prod_cat_sub_name.like(w)))#.paginate(page,customer_config.PROD_NUM_PER_PAGE, False)

        # print(prod_list_query)
        prod_list_all = prod_list_query.order_by(Prod_info.prod_id).all()#supplier.supplier_name
        supplier_list = set([p.supplier for p in prod_list_all])
        supplier_list = sorted(supplier_list,key=lambda x:x.supplier_id)

        if supplier_id:
            prod_list_query = prod_list_query.filter_by(supplier_id=supplier_id)

        prod_list = prod_list_query.paginate(page,current_app.config.get("PROD_NUM_PER_PAGE"), False)
        pagination = Pagination(page=page, total=prod_list.total,
                                search=None, css_framework='bootstrap3',
                                record_name='Prod Information',
                                per_page=current_app.config.get("PROD_NUM_PER_PAGE"))

        return prod_list,supplier_list,pagination


def order_search_filter(keyword,query_base,page):
    if keyword and query_base:
        w = "%{keyword}%".format(keyword=keyword)
        s = Session()
        order_list_query = query_base.filter(or_(Order_system.order_id.like(w),
                                                Order_system.client_order_id.like(w),
                                                Order_system.prod_name.like(w)))

        order_list = order_list_query.paginate(page,current_app.config.get("USER_ORDER_PER_PAGE"), False)
        pagination = Pagination(page=page, total=order_list.total,
                                search=None, css_framework='bootstrap3',
                                record_name='Prod Information',
                                per_page=current_app.config.get("USER_ORDER_PER_PAGE"))

        return order_list,pagination

def quote_search_filter(keyword,query_base,page):
    if keyword and query_base:
        w = "%{keyword}%".format(keyword=keyword)
        s = Session()
        quote_list_query = query_base.filter(or_(Quote_system.quote_id.like(w),
                                                Quote_system.prod_name.like(w)))

        quote_list = quote_list_query.paginate(page,current_app.config.get("USER_QUOTE_PER_PAGE"), False)
        pagination = Pagination(page=page, total=quote_list.total,
                                search=None, css_framework='bootstrap3',
                                record_name='Prod Information',
                                per_page=current_app.config.get("USER_QUOTE_PER_PAGE"))

        return quote_list,pagination