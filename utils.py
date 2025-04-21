import re
import hashlib
import random
import time
import threading

def get_numeric_files(files):
    """
    Retorna os arquivos e seu número correspondete.
    
    Retorna uma lista de dicionários, onde cada dicionário contém:
    - 'file': o arquivo original
    - 'number': a parte numérica extraída do nome
    """
    numeric_files = []
    pattern = re.compile(r"^(\d+)\..+$") 

    for f in files:
        match = pattern.match(f['name'])
        if match:
            numeric_files.append({'file': f, 'number': int(match.group(1))})

    if numeric_files:
        max_number = max(numeric_files, key=lambda x: x['number'])['number']


        max_number_files = [f for f in numeric_files if f['number'] == max_number]


        min_timestamp_file = min(max_number_files, key=lambda x: x['file']['createdTime'])

        return min_timestamp_file

    return numeric_files

def proof_of_work(previous_hash, name, drive, difficulty=4):
    nonce = random.uniform(1, 100)
    prefix = '0' * difficulty 
    request = 50000

    while True:
        data = f"{previous_hash}{nonce}".encode()  
        new_hash = hashlib.sha256(data).hexdigest() 
        

        if (request == 0):
                files = drive.files().list(
                    pageSize=1,
                    fields="files(id, name, createdTime)",
                    orderBy="createdTime desc"
                ).execute().get('files', [])
                
                print(files)
                name_goal = files[0]['name'].split('.')[0]
                if (name_goal == name):
                    print("-------------_________________________!!!!!!!!!!!!!!!!!!PAREI DE BUSCAR -------------_________________________!!!!!!!!!!!!!!!!!!")
                    return ("NONE", "NONE")
                
                request = 50000
        
        request -= 1

        if new_hash.startswith(prefix):
            print(f"PoW resolvido! Nonce: {nonce}, Hash: {new_hash}")
            return new_hash, nonce

        nonce += 1  

def get_numeric_files_level(files, level):
    out = []

    name = str(level)+".txt"

    for file in files:
        if (file['name'] == name):
            out.append(file)
    
    return out