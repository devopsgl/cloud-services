import requests
from flask import Flask, jsonify, Response
from ruamel.yaml import YAML
import sys
import time
def putValues(GIT_API_URL,GIT_ACCESS_TOKEN,repositoryId,repository_tag,user_group_id,serviceName):
    PROJECT_ID = repositoryId
    # Export işlemini başlat
    headers = {
        "PRIVATE-TOKEN": GIT_ACCESS_TOKEN
    }
    export_url = f"{GIT_API_URL}projects/{PROJECT_ID}/export"
    print("exportttt",export_url,flush=True)
    response = requests.post(export_url, headers=headers)
    if response.status_code == 202:
        print("Export işlemi başlatıldı.")
    else:
        print(f"Export işlemi başlatılamadı: {response.status_code} {response.text}")
        exit()

    # Export işleminin tamamlanmasını bekle
    export_status_url = f"{GIT_API_URL}/projects/{PROJECT_ID}/export"
    while True:
        response = requests.get(export_status_url, headers=headers)
        if response.status_code == 200:
            export_status = response.json()
            if export_status['export_status'] == 'finished':
                print("Export işlemi tamamlandı.")
                break
            elif export_status['export_status'] == 'failed':
                print("Export işlemi başarısız oldu.")
                exit()
        else:
            print(f"Export durumunu kontrol edemedim: {response.status_code} {response.text}")
            exit()
        time.sleep(5)

    # Export edilmiş dosyayı indir
    download_url = export_status['_links']['api_url']
    response = requests.get(download_url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(f'/tmp/{serviceName}.tar.gz', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Export edilen dosya /tmp dizinine kaydedildi.")
        with open(f'/tmp/{serviceName}.tar.gz', 'rb') as file:
            files = {
                'file': file
            }
            response = requests.post(f"{GIT_API_URL}/projects/import", headers=headers, files=files)

        if response.status_code == 201:
            print("Proje başarıyla yüklendi.")
        else:
            print(f"Proje yüklenemedi: {response.status_code} {response.text}")

        # Import işlemini tamamlamak için gerekli parametreleri gönderme
        data = {
            'namespace': user_group_id,  # Grubun kimliği
            'path': serviceName,  # Yeni proje adı
            'overwrite': 'true'  # Mevcut proje üzerine yazmak için
        }

        response = requests.post(f"{GIT_API_URL}/projects/import", headers=headers, data=data)

        if response.status_code == 202:
            print("Import işlemi başlatıldı.")
        else:
            return f"Import işlemi başlatılamadı: {response.status_code} {response.text}"
    else:
        print(f"Export edilen dosya indirilemedi: {response.status_code} {response.text}")
        return "Export edilen dosya indirilemedi"
