# #from flask_admin.contrib.sqla import ModelView
# import flask_admin
# from flask_admin.contrib import sqla
# from webapp.Models.user import User
# from webapp.Models.db_basic import Session
# import flask_login as login
# from flask import redirect,url_for,request,flash
# from webapp.viewrouting.user.forms import login_form,registeration_form
# from webapp.common import generate_md5
# #from werkzeug.security import generate_password_hash
#
# # TODO Can customized permission control for any view using below sample code
# # def UserModelView(ModelView):
# #     def is_accessible(self):
# #
# #         return True
# #
# #     def inaccessible_callback(self, name, **kwargs):
# #         # redirect to login page if user doesn't have access
# #         return redirect(url_for('user.login', next=request.url))
#
# class MyAdminIndexView(flask_admin.AdminIndexView):
#
#     @flask_admin.expose('/')
#     def index(self):
#         if not login.current_user.is_authenticated :
#             return redirect(url_for('userRoute.admin_login'))
#         if  not login.current_user.is_admin :
#             flash("Access denied ! Please use admin id!")
#             login.logout_user()
#             return redirect(url_for('userRoute.admin_login'))
#         return super(MyAdminIndexView, self).index()
#
#     @flask_admin.expose('/login/', methods=('GET', 'POST'))
#     def login_view(self):
#         # handle user login
#         form = login_form.LoginForm # LoginForm(request.form)
#         if flask_admin.helpers.validate_form_on_submit(form):
#             user = form.get_user()
#             login.login_user(user)
#
#         #TODO this should be chagned to check whether the user has a particular role
#         if login.current_user.is_authenticated :
#             if login.current_user.is_admin :
#                 return redirect(url_for('.index'))
#             else:
#                 flash("Access denied ! Please use admin id!")
#                 login.logout_user()
#                 return redirect(url_for('userRoute.admin_login'))
#         else:
#             flash("User ID or Password invalid.")
#             return redirect(url_for('userRoute.admin_login'))
#         link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
#         self._template_args['form'] = form
#         self._template_args['link'] = link
#         return super(MyAdminIndexView, self).index()
#
#     @flask_admin.expose('/register/', methods=('GET', 'POST'))
#     def register_view(self):
#         #TODO View needs to be created
#         form = registeration_form.RegistrationForm(request.form)
#         if flask_admin.helpers.validate_form_on_submit(form):
#             user = User()
#
#             form.populate_obj(user)
#             # we hash the users password to avoid saving it as plaintext in the db,
#             # remove to use plain text:
#             passwd = generate_md5(form.password.data)
#             user.password =  passwd# generate_password_hash(form.password.data)
#             session = Session()
#             session.add(user)
#             session.commit()
#
#             login.login_user(user)
#             return redirect(url_for('.index'))
#         link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
#         self._template_args['form'] = form
#         self._template_args['link'] = link
#         return super(MyAdminIndexView, self).index()
#
#     @flask_admin.expose('/logout/')
#     def logout_view(self):
#         login.logout_user()
#         return redirect(url_for('.index'))
#
#
# def register_admin_view(admin):
#     admin.add_view(sqla.ModelView(User, Session()))
#
