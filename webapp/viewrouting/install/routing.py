# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template
from webapp.viewrouting.install.forms import deploy_config
import os, string

from webapp.common import generate_security_key,generate_md5

installRoute = Blueprint('installRoute', __name__,
                         template_folder='install_temp', static_folder='static')

#TODO : use this installation program to config the structrue of the whole application

@installRoute.route('/', methods=['GET', 'POST'])
def index():
    config_form = deploy_config.Deploy_Config()
    if config_form.validate_on_submit():
        import webapp as w
        config_folder = os.path.dirname(w.__file__)
        config_file = config_folder + os.sep + 'config.py'
        generate_config_file(config_form, config_file)
        create_meta_db(config_form)

        return render_template('success.html')
    else:
        return render_template('index.html', form=config_form)


# generate config file
def generate_config_file(form, config_file):
    content_template = string.Template('''
#DB INFORMATION
META_DB={
    'DB_TYPE':'$db_type',
	'DB_HOST':'$db_ip',
	'DB_PORT':$db_port,
	'DB_USER':'$db_user',
	'DB_PASSWORD':'$db_passwd',
	'DB_NAME':'$db_name'

}


#DEBUF INFORMATION
DEBUG = $debug

#SECURITY
SECRET_KEY = '$secret_key'

#APPLICATION NAME
APP_NAME = '$app_name'

#BIND INFORMAITON
HOST = '$server_ip'
PORT = $server_port

    ''')
    content = content_template.safe_substitute(db_type=form.db_type.data,
                                               db_ip=form.db_ip.data,
                                               db_port=form.db_port.data,
                                               db_user=form.db_user.data,
                                               db_passwd=form.db_passwd.data,
                                               db_name=form.db_name.data,
                                               debug=form.debug.data,
                                               secret_key=generate_security_key(60),
                                               app_name=form.app_name.data,
                                               server_ip=form.server_ip.data,
                                               server_port=form.server_port.data)
    with open(config_file, 'w') as f:
        f.write(content)

    return content


# create admin user
def create_meta_db(config_form):
    import webapp.Models.db_init as db_init  # import recreate_all,User
    import webapp.Models as db

    db_init.recreate_all()

    admin = db.User()
    admin.nickname = config_form.admin_id.data
    admin.is_admin = True
    admin.email = config_form.admin_email.data

    passwd = generate_md5(config_form.admin_passwd.data) #hashlib.md5(config_form.admin_passwd.data.encode('ascii'))
    admin.password = passwd
    #admin.password = generate_password_hash(config_form.admin_passwd.data)

    s = db.Session()
    s.add(admin)
    s.commit()
