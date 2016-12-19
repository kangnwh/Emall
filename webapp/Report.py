import os,sys
sys.path.append(os.path.dirname(os.getcwd()))

#flask related packages
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

#blueprint
from webapp.viewrouting.home.routing import homeRoute
from webapp.viewrouting.user.routing import userRoute
from webapp.viewrouting.admin.routing import adminRoute
#Models
from webapp.Models.db_basic import Session
from webapp.Models.user import User,AnonymousUser

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
    (adminRoute,'/admin')
}


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)
app.config.from_pyfile('customer_config.py', silent=False)
bootstrap = Bootstrap(app)
login_manager.init_app(app)
mail.init_app(app)


for module,url_prefix in Report_Modules:
    app.register_blueprint(module, url_prefix=url_prefix)

@login_manager.user_loader
def load_user(user_id):
    s = Session()
    return s.query(User).filter_by(user_id=user_id).first()

if __name__ == '__main__':
    # app = create_app()
    app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get("PORT", "5002"), threaded=True)

def create_app():
    return app