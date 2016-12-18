import random
import hashlib
from webapp.Models.db_basic import Session
from webapp.Models.prod_cat import Prod_cat
from webapp.Models.prod_sub_cat import Prod_sub_cat
import os
from flask_login import current_user,login_required
from flask import flash,redirect,url_for
from webapp.customer_config import ALLOWED_EXTENSIONS
from PIL import Image
from webapp.customer_config import USER_LOGO_UPLOAD_PATH
from werkzeug import secure_filename
import datetime
from webapp.customer_config import PROD_UPLOAD_PATH,ALLOWED_EXTENSIONS

def generate_security_key(key_len):
    pwdStrPool = '0123456789'\
    'abcdefghijkmnpqrstuvwxyz'\
    '~@#$%^&*()_+|'\
    'ABCDEFGHIJKMNPQRSTUVWXYZ'
    array_len = len(pwdStrPool)
    security_key = [pwdStrPool[i] for i in (random.randint(0,array_len-1) for x in range(key_len))]
    return ''.join(security_key)

def generate_md5(data):
    md5 = hashlib.md5(data.encode('ascii'))
    return md5.hexdigest()

def generate_sidebar():
    first_level_list=list()
    first_level_list.append('<aside ><section  class="sidebar">	    <ul class="sidebar-menu">	      <li class="header">Navigation</li>')
    s = Session()
    category_list = s.query(Prod_cat).filter_by(valid_flg=1).order_by(Prod_cat.prod_cat_order)

    for first_level in category_list:
        first_level_list.append('''
        <li class="treeview {{% if {prod_cat_id}== nav_active %}}active{{% endif %}}"><a href="#"> <i class="fa fa-dashboard"></i> <span>{cat_name}</span> <i class="fa fa-angle-left pull-right"></i></a>
        '''.format (prod_cat_id=first_level.prod_cat_id,cat_name=first_level.prod_cat_name))

        first_level_list.append( '<ul class="treeview-menu">')

        for second_level in first_level.prod_sub_cat:
            first_level_list.append('<li><a href="{{ url_for("homeRoute.sub_category_list",sub_cat_id=%s) }}"><i class="fa fa-circle-o"></i>%s</a></li>' % (second_level.prod_cat_sub_id,second_level.prod_cat_sub_name))

        first_level_list.append('</ul></li>')

    first_level_list.append('</ul></section></aside>')

    content = ''.join(first_level_list)

    import webapp as w
    sidebar_template_folder = os.path.dirname(w.__file__)
    sidebar_template = sidebar_template_folder + os.sep + 'templates' +os.sep + 'sidebar.html'
    with open(sidebar_template, 'w') as f:
        f.write(content)

    return content


def admin_check(func):
    def real_func(*args,**kwargs):
        if current_user.is_administrator:
            ret = func(*args,**kwargs)
            return ret
        else :
            flash("You are not an administrator for this system, please use an admin id.",category='danger')
            return redirect(url_for("userRoute.login"))

    return real_func

def allowed_file(filename):


    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

def saveImage(request_file,prod):
     if  request_file.filename :
            if allowed_file(request_file.filename):
                    filename = "{prod_name}{time}.{ext}".format( prod_name=prod.prod_name ,
                                                                 time=datetime.datetime.now().isoformat().replace(':','_').replace('.','_') ,
                                                                 ext=secure_filename(request_file.filename)[-3:])
                    request_file.save(os.path.join(PROD_UPLOAD_PATH, filename))
                    return filename
            else :
                    flash("Only accept {types} file".format(types=ALLOWED_EXTENSIONS),category='danger')

     return False


def generatePNG(image):
    img = Image.open(USER_LOGO_UPLOAD_PATH+image)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] >= 220 and item[1] >= 220 and item[2] >= 220:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(USER_LOGO_UPLOAD_PATH+'GEN_'+image, "PNG")


def object2dict(obj):
    #convert object to a dict
    d = {}
    #d['__class__'] = obj.__class__.__name__
    #d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d