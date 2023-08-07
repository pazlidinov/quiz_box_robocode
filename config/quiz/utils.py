from django.contrib.auth.base_user import BaseUserManager
import json
import requests

def make_access_password(request):
    password=BaseUserManager().make_random_password(6)
    request.session['lead_user_password']=password   
    data = {
        'send':'',
        'number':request.POST.get('phone'),
        'text':'Access code: '+password,
        'token':'THpraofsxAqQnkjOPEFSdmeLvRKNluhtbBZXVyIUGiDJYMg',
        'id':212,
        'user_id':'1257603816'
        }
    data_json = json.dumps(data)  
    r = requests.post('https://api.xssh.uz/smsv1/?data='+ data_json)
    status=r.text.split(',')[-1].split(':')[-1][:-1]
    if status == "200":       
        return True
    else: 
        return False