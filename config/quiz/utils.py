import json
import requests
from datetime import datetime, timedelta, date
from random import randint


def make_access_password(number, password):
    data = {
        'send': '',
        'number': number,
        'text': 'Access code: '+str(password),
        'token': 'THpraofsxAqQnkjOPEFSdmeLvRKNluhtbBZXVyIUGiDJYMg',
        'id': 212,
        'user_id': '1257603816'
    }
    data_json = json.dumps(data)
    r = requests.post('https://api.xssh.uz/smsv1/?data=' + data_json)
    status = r.text.split(',')[-1].split(':')[-1][:-1]
    # status = '200'
    if status == "200":
        return True
    else:
        return False


def control_send(user):
    # time_delta = timedelta(minutes=30)
    # t = user.date_time
    # delta=(datetime.combine(date(1, 1, 1), t) + time_delta).time()
    # if delta >= datetime.now().time() and user.send_count < 4:
    password = randint(100000, 999999)
    print(password)
    if make_access_password(user.phone, password):
        user.change_password(password)
        user.send_plus
        return True
    else:
        return False


def control_user(user):
    if user.is_authenticated:
        return True
    else:
        return False
