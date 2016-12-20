from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os,sys

cur_path = os.getcwd()
sys.path.append(cur_path)

# try:
#     from webapp import config
#     from webapp import Report
#
#     app = Report.create_app()
#     app.logger.info("main application run")
#     app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get("PORT", "5001"), threaded=True)
# except:
#     from webapp import Install
#     app = Install.create_app()
#     app.logger.info("installation application run")
#     app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get("PORT", "5001"), threaded=True)
