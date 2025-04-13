import os
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from utils import get_numeric_files, proof_of_work
import random
import time
import threading
import io
from datetime import datetime
import json

def get_largest_numbered_file(drive):
    """Encontra o arquivo com o maior número no nome e retorna seus metadados."""

    sleep_time = random.uniform(0.5, 30)
    print(f"Thread {threading.current_thread().name} dormindo por {sleep_time:.2f} segundos...")
    time.sleep(sleep_time)
    print(f"Thread {threading.current_thread().name} acordou e está processando...")


    
    files = drive.files().list(
        pageSize=10,
        fields="files(id, name, createdTime)",
        orderBy="createdTime desc"
    ).execute().get('files', [])
    print("FIels: ")
    print(files)
    numeric_files = get_numeric_files(files)
    
    if not numeric_files:
        print("Nenhum arquivo encontrado.")
        return 0
      
    most_recent_file =  numeric_files
    print("Most recent file:")
    print(most_recent_file)
    return most_recent_file  

def create_and_upload_new_file(drive, max_file):
    """Cria um novo arquivo com um número maior e faz upload para o Google Drive."""
    max_number = max_file['number']
    new_number = max_number + 1
    new_file_name = f"{new_number}"

    request = drive.files().get_media(fileId=max_file['file']['id'])
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)

    done = False    
    while not done:
        _, done = downloader.next_chunk()

    file_stream.seek(0) 
    content = file_stream.read().decode("utf-8")  

    contentDict = json.loads(content)
    
    
    hash, nonce = proof_of_work(content, new_file_name, drive)  
    if (hash == "NONE"):
        return 0
     
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Midia:")
    print(content)
    print("Hash")
    print(hash)

    temp_file_path = f"{new_file_name}.txt"
    dict = {
            'hash': hash,
            'previous_hash': contentDict['hash'],
            'timestamp': timestamp_str,
            'nonce' : nonce
    }
    with open(temp_file_path, "w") as f:
        f.write(json.dumps(dict))

    media = MediaFileUpload(temp_file_path, mimetype='text/plain')
    
    new_metadata = {'name': temp_file_path, 'mimeType': 'text/plain'}
    uploaded_file = drive.files().create(body=new_metadata, media_body=media, fields='id').execute()
    
    print(f"Novo arquivo enviado: {new_file_name} (ID: {uploaded_file['id']})")
    
    if open(temp_file_path, "w"):
        os.remove(temp_file_path)