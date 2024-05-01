import requests

def storeList(GIT_API_URL,GIT_ACCESS_TOKEN):
    url = f"{GIT_API_URL}/groups/application-store/projects"
    headers = {
        'Private-Token': GIT_ACCESS_TOKEN,
    }
    try:
        response = requests.get(url, headers=headers)
        result ={
            "code": "",
            "msg": ""

        }
        if response.status_code == 200:
            projects = response.json()
            filtered_data = []

            for item in projects:
                id= item['id']
                name= item['name']
                tags_url =f"{GIT_API_URL}projects/{id}/repository/tags"
                response=requests.get(tags_url,headers=headers)
                tags=response.json()
                filtered_tags =[item['name'] for item in tags]
                tags ={"tags": filtered_tags}
                print (tags)
                data = {
                    'id': id,
                    'name': name,
                    
                }
                data.update(tags)   
                filtered_data.append(data) 
            return filtered_data
        else:
            result['code']=response.status_code
            result['msg']="failed"
            return result
        
    except requests.exceptions.RequestException as e:
            print (e)
            return {'code':'err', 'msg': 'connection refused'}