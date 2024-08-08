import requests,os

GIT_API_URL = os.getenv('GIT_API_URL', 'no url') 
GIT_ACCESS_TOKEN = os.getenv('GIT_ACCESS_TOKEN', 'no token') 

def createGroup(userId):
    url = f"{GIT_API_URL}/groups"
    headers = {
        'Authorization': 'Bearer ' + GIT_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'name': userId,
        'path': userId,
        'description': 'Açıklama',
        'visibility': 'private'  
    }
    result ={
        "code": "",
        "msg": ""
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print("Grup başarıyla oluşturuldu.")
            print(response.json())
            result['code']=response.status_code
            result['msg']=response.text
            return result
        else:
            result['code']=response.status_code
            result['msg']=response.text
            print(response.text)
            return result
    except requests.exceptions.RequestException as e:
            print (e)
            return {'code':'err', 'msg': 'connection refused'}
