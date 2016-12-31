import os,sys
sys.path.append(os.path.dirname(os.getcwd()))

#flask related packages
from flask import Flask,redirect,request,flash,url_for
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

#blueprint
from webapp.viewrouting.home.routing import homeRoute
from webapp.viewrouting.user.routing import userRoute
from webapp.viewrouting.admin.routing import adminRoute
from webapp.viewrouting.order.routing import orderRoute
from webapp.common import get_host_info
#Models
from webapp.Models.db_basic import Session
from webapp.Models.user import User,AnonymousUser
from webapp.Models import get_pending_order_count,get_pending_quote_count

#flask mail
import flask_mail
mail = flask_mail.Mail()

login_manager = LoginManager()
login_manager.login_view="userRoute.login"
login_manager.anonymous_user = AnonymousUser

#Modules
Report_Modules={
    (homeRoute, ''),
    (userRoute,'/user'),
    (adminRoute,'/admin'),
    (orderRoute,'/orders')
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
def load_user(user_id):
    s = Session()
    u = s.query(User).filter_by(user_id=user_id).first()
    if u:
        u.get_pending_order_count = lambda id : get_pending_order_count('user',user_id)
        u.get_pending_quote_count = lambda id : get_pending_quote_count('user',user_id)
    # u.pending_ordr_count = u.user_order_sys.total()
    return u

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please Login First",'danger')
    return redirect(url_for("userRoute.register_login",next=request.path))

if __name__ == '__main__':
    # app = create_app()
    ip,port = get_host_info('HOME_HOST')
    app.run(host=ip, port=port, threaded=True)

def create_app():
    return app