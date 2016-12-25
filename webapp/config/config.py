
# DB INFORMATION
META_DB = {
    'DB_TYPE': 'mysql',
    'DB_HOST': '106.14.31.132',
    'DB_PORT': 3306,
    'DB_USER': 'emall',
    'DB_PASSWORD': 'dbpw4LS!',
    'DB_NAME': 'emall'

}

# DEBUF INFORMATION
DEBUG = True

# SECURITY
SECRET_KEY = 'Du#Sy6j@peK~egjvrC$90nu7eK2K_#iA@CI0)mhJwkf2Pk_AWZakp$a&(FM*'

# APPLICATION NAME
APP_NAME = 'Emall'

# BIND INFORMAITON
HOST_INFO={
    'HOME_HOST':{
        'IP':'106.14.31.132',
        'PORT':5002
    },
    'SUPPLIER_HOST':{
         'IP':'106.14.31.132',
        'PORT':5003
    }
}
# user discount rate
USER_POINT_DISCOUNT_RATE = 0.01
#Reminders should be sent %d days before end date
REMINDER_PRE_DAYS = 3