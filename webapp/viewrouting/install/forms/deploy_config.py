from flask_wtf import Form
from wtforms import StringField,IntegerField,PasswordField,BooleanField,SelectField
from wtforms.validators import DataRequired, ValidationError
from webapp.install_config import SUPPORT_DB
def is_ip_connectable(form,field):
        return True

class Deploy_Config(Form):
    db_type = SelectField('数据库类型',choices=[(x,x) for x in SUPPORT_DB],validators=[DataRequired(message='请选择数据库类型')])
    db_ip = StringField('数据库IP',validators=[DataRequired(message='请输入数据库IP'),is_ip_connectable])
    db_port = IntegerField('数据库端口',validators=[DataRequired(message='请输入数据库端口')])
    db_name = StringField('数据库名称',validators=[DataRequired(message='请输入数据库名称')])
    db_user = StringField('数据库用户',validators=[DataRequired(message='请输入数据库用户')])
    db_passwd = PasswordField('数据库密码',validators=[DataRequired(message='请输入数据库密码')])


    app_name = StringField('系统名称',validators=[DataRequired(message='请设置要为系统启的名称')])
    server_ip = StringField('系统对外绑定的IP',validators=[DataRequired(message='请设置系统对外开放的IP')])
    server_port = IntegerField('系统对外的端口号',validators=[DataRequired(message='请设置系统对外开放的端口号')])
    admin_id = StringField('系统管理员帐号',validators=[DataRequired(message='请设置系统管理员帐号')])
    admin_email = StringField('系统管理员邮箱',validators=[DataRequired(message='请设置系统管理员邮箱')])
    admin_passwd = PasswordField('系统管理员密码',validators=[DataRequired(message='请设置系统管理员密码')])
    debug = BooleanField('开发者模式',validators=[DataRequired(message='请选择是否启用debug')])


