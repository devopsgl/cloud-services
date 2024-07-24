import requests
import os
import zipfile
import tempfile
import shutil
import uuid
import base64
import urllib.parse
import sys
from flask import Flask, request, jsonify

# Fonksiyon: Dosya içeriğini okuma
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Fonksiyon: Dosyaları ve klasörleri toplayıp, API isteğine hazır hale getirme
def prepare_actions(base_dir):
    actions = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_gitlab_path = os.path.relpath(file_path, base_dir).replace('\\', '/')
            actions.append({
                #"action": "update",
                "file_path": file_gitlab_path,
                "content": read_file_content(file_path)
            })
    return actions

# API isteği: Commit oluşturma
def commit_to_gitlab(GIT_API_URL,project_id, commit_message, actions, access_token):
    url = f'{GIT_API_URL}projects/{project_id}/repository/commits'
    headers = {
        'PRIVATE-TOKEN': access_token,
        'Content-Type': 'application/json'
    }
    data = {
        'branch': 'main',
        'commit_message': commit_message,
        'actions': actions
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print('Commit başarılı!')
        return "successss"
    else:
        print('Commit başarısız:', response.json())
        return actions

def get_project_id(GIT_API_URL,group_id, project_name, access_token):
    url = f'{GIT_API_URL}groups/{group_id}/projects'
    headers = {
        'PRIVATE-TOKEN': access_token
    }
    params = {
        'search': project_name
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project['name'] == project_name:
                return project['id']
        return None
    else:
        print('Proje ID\'si alınamadı:', response.json())
        return None


def putValues(GIT_API_URL,GIT_ACCESS_TOKEN,repositoryId,repository_tag,user_group_id,serviceName,values_content):
    DOWNLOAD_DIR = '/tmp'

    if not values_content:
        return jsonify({"error": "No content provided"}), 400


    unique_id = str(uuid.uuid4())
    unique_extract_dir = os.path.join(DOWNLOAD_DIR, unique_id)
    os.makedirs(unique_extract_dir, exist_ok=True)

    # values.yaml dosyasını geçici bir dosyaya kaydet
    values_file_path = os.path.join(unique_extract_dir, 'values.yaml')
    with open(values_file_path, 'w') as f:
        f.write(values_content)


    # GitLab kişisel erişim tokenı
    # Header bilgisi
    headers = {
        'PRIVATE-TOKEN': GIT_ACCESS_TOKEN
    }

    # API endpoint'i
    url = f"{GIT_API_URL}/projects/{repositoryId}/repository/archive.zip?sha={repository_tag}"

    # Tag arşivini indirme
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
         return jsonify({"error": f"Failed to download project archive. HTTP Status Code: {response.status_code}"}), 500

     # Geçici bir dosyaya zip içeriğini yazın
    temp_zip = tempfile.NamedTemporaryFile(delete=False, dir=unique_extract_dir)
    temp_zip.write(response.content)
    temp_zip.close()

    # Zip dosyasını açın ve içeriğini çıkarın
    with zipfile.ZipFile(temp_zip.name, 'r') as zip_ref:
        zip_ref.extractall(unique_extract_dir)

    # Geçici zip dosyasını silin
    os.remove(temp_zip.name)
    # Çıkarılan zip dosyasındaki yeni klasörün adını bulun
    # Çıkarılan zip dosyasındaki yeni klasörün adını bulun
    extracted_items = os.listdir(unique_extract_dir)
    extracted_folder_name = None
    for item in extracted_items:
        if os.path.isdir(os.path.join(unique_extract_dir, item)):
            extracted_folder_name = item
            break
    
    if not extracted_folder_name:
        return jsonify({"error": "Failed to find extracted folder"}), 500

    extracted_folder_path = os.path.join(unique_extract_dir, extracted_folder_name)

    # values.yaml dosyasını çıkarılan proje klasörüne kopyalayın
    extracted_values_path = os.path.join(extracted_folder_path, 'values.yaml')
    shutil.copy(values_file_path, extracted_values_path)



    ##----
   # Yeni bir proje oluşturun
    new_project_name = f"{repository_tag}_updated"
    new_project_response = requests.post(
        f"{GIT_API_URL}/projects",
        headers=headers,
        json={
            "name": serviceName,
            "namespace_id": user_group_id  # Bu projeyi oluşturmak istediğiniz namespace ID
        }
    )

    if new_project_response.status_code != 201:
        new_project_id=get_project_id(GIT_API_URL,user_group_id,serviceName,GIT_ACCESS_TOKEN)
        action_state="update"
    else:
        new_project_id = new_project_response.json()['id']
        action_state="create"



    # Yeni projeye dosyaları yükleyin

    #return f"{extracted_folder_path}"

    actions = prepare_actions(extracted_folder_path)
    for action in actions:
        file_path = action["file_path"]
        file_path= urllib.parse.quote(file_path,safe='')

        sys.stdout.write(f" {file_path} Hello, World!\n")
        sys.stdout.flush()

        file_exists_url = f'{GIT_API_URL}/projects/{new_project_id}/repository/files/{file_path}?ref=main'
        headers = {
            'PRIVATE-TOKEN': GIT_ACCESS_TOKEN
        }
        response = requests.get(file_exists_url, headers=headers)
        if response.status_code == 200:
            action["action"] = "update"
        else:
            action["action"] = "create"

    return commit_to_gitlab(GIT_API_URL,new_project_id, "cloud services", actions, GIT_ACCESS_TOKEN)

    




