import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

#flask related packages
from flask import Flask,redirect,request,flash,url_for
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

#blueprint
from webapp.supplierrouting.home.routing import homeRoute
from webapp.supplierrouting.admin.routing import supplierRoute
from webapp.supplierrouting.user.routing import userRoute
from webapp.supplierrouting.order.routing import orderRoute
from webapp.common import get_host_info
#Models
from webapp.Models import get_pending_order_count,get_pending_quote_count,get_supplier_level
from webapp.Models.db_basic import Session
# from webapp.Models.user import User,AnonymousUser
from webapp.Models.supplier import Supplier,AnonymousSupplier
from webapp.Models import get_pending_order_count,get_pending_quote_count,get_approval_pending_count,get_approval_pending_advertisment
#flask mail
import flask_mail
mail = flask_mail.Mail()

login_manager = LoginManager()
login_manager.login_view="userRoute.register_login"
login_manager.anonymous_user = AnonymousSupplier

#Modules
Report_Modules={
    (supplierRoute, ''),
    (homeRoute,'/prod'),
    (userRoute,'/supplier'),
    (orderRoute,'/order')
}


app = Flask(__name__)
app.config.from_pyfile('config/config.py', silent=False)
app.config.from_pyfile('config/customer_config.py', silent=False)
bootstrap = Bootstrap(app)
login_manager.init_app(app)
mail.init_app(app)


for module,url_prefix in Report_Modules:
    app.register_blueprint(module, url_prefix=url_prefix)

@login_manager.user_loader
def load_user(supplier_id):
    s = Session()
    u = s.query(Supplier).filter_by(supplier_id=supplier_id).first()
    if u:
        u.get_pending_order_count = lambda id : get_pending_order_count('supplier',supplier_id)
        u.get_pending_quote_count = lambda id : get_pending_quote_count('supplier',supplier_id)
        u.get_supplier_level = lambda id : get_supplier_level('supplier',supplier_id)
        u.get_approval_pending_count = lambda id : get_approval_pending_count('supplier',supplier_id)
        u.get_approval_pending_advertisment = lambda id : get_approval_pending_advertisment('supplier',supplier_id)
    s.close()
    return u

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please Login First",'danger')
    return redirect(url_for("userRoute.register_login",next=request.path))

if __name__ == '__main__':
    # app = create_app()
    emall_ip, emall_port = get_host_info('HOME_HOST')
    supplier_ip, supplier_port = get_host_info('SUPPLIER_HOST')
    app.config["EMALL_APPLICATION_ADDRESS"] = "http://{emall_ip}:{emall_port}".format(emall_ip=emall_ip,emall_port = emall_port )
    app.config["SUPPLIER_APPLICATION_ADDRESS"] = "http://{supplier_ip}:{port}".format(supplier_ip=supplier_ip,port = supplier_port )
    app.run(host=supplier_ip, port=supplier_port, threaded=True)

def create_app():
    return app