#flask related packages
from flask import Flask
from flask_bootstrap import Bootstrap

#blueprint
from webapp.viewrouting.install.routing import installRoute

bootstrap = Bootstrap()



#Modules
Report_Modules={
    (installRoute, ''),
}


#create app and config app
def create_app(config_file='install_config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file, silent=False)
    bootstrap.init_app(app)
    for module,url_prefix in Report_Modules:
        app.register_blueprint(module, url_prefix=url_prefix)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get("PORT", "5002"), threaded=True)
