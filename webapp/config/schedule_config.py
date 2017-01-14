from webapp.common.mails import deliver_notification
JOBS = [
        {
            'id': 'deliver_notification',
            'func': deliver_notification,
            'args': None,
            'trigger': 'interval',
            'seconds': 10
        }
    ]