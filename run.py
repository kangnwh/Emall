from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os,sys

cur_path = os.getcwd()
sys.path.append(cur_path)
sys.path.append("{base}{sep}webapp".format(base=cur_path,sep=os.sep))

try:
    from webapp.emall_run import run_app as run_emall_app
    from webapp.emall_supplier_run import run_app as run_supplier_app
    if sys.argv[1] == 'emall':
        app = run_emall_app()
    elif sys.argv[1] == 'supplier':
        app = run_supplier_app()
    else:
        print("run with arg = 'emall' or 'supplier'")
except:
    print("Start error")
