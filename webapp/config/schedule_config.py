from webapp.common.mails import deliver_notification
from flask_apscheduler import APScheduler
scheduler = APScheduler()


SCHEDULER_API_ENABLED = False
JOBS = [
        {
            'id': 'deliver_notification',
            'func': deliver_notification,
            'args': None,
            'trigger': 'cron',
            'hour': 15,
            'minute':27,
            'second':0
        }
    ]

