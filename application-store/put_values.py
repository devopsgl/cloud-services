import requests
import os
import zipfile
import tempfile
import shutil
import uuid
import base64
from flask import Flask, request, jsonify
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
        return jsonify({"error": f"Failed to create new project. HTTP Status Code: {new_project_response.text}"}), 500

    new_project_id = new_project_response.json()['id']

    # Yeni projeye dosyaları yükleyin

    #return f"{extracted_folder_path}"

    def upload_file_to_gitlab(project_id,file_path, gitlab_path):
        with open(file_path, 'rb') as file:
            content = base64.b64encode(file.read()).decode('utf-8')

        url = f"{GIT_API_URL}/api/v4/projects/{project_id}/repository/files/{gitlab_path}"
        headers = {
            'PRIVATE-TOKEN': GIT_ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }
        data = {
            'branch': "main",
            'content': content,
            'commit_message': f'Add {gitlab_path}'
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print(f'Successfully uploaded {gitlab_path}')
        elif response.status_code == 400:
            print(f'File already exists: {gitlab_path}. Updating file...')
            response = requests.put(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f'Successfully updated {gitlab_path}')
            else:
                print(f'Failed to update {gitlab_path}. Response: {response.json()}')
        else:
            print(f'Failed to upload {gitlab_path}. Response: {response.json()}')


    upload_file_to_gitlab(new_project_id,extracted_folder_path,"/")

    def upload_directory_to_gitlab(directory, gitlab_path=''):
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, directory)
                gitlab_file_path = os.path.join(gitlab_path, relative_path).replace('\\', '/')
                upload_file_to_gitlab(file_path, gitlab_file_path)

    upload_directory_to_gitlab(extracted_folder_path)





    # Geçici dizini silin
    shutil.rmtree(unique_extract_dir)

    return jsonify({
        "message": f"New project '{new_project_name}' created successfully.",
        "extracted_path": extracted_folder_path  # Çıkarılan klasörün yolunu da döndürün
    }), 201

