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
    pattern = re.compile(r"^(\d+)\..+$")  # Captura apenas arquivos no formato número.extensão

    for f in files:
        match = pattern.match(f['name'])
        if match:
            numeric_files.append({'file': f, 'number': int(match.group(1))})

    if numeric_files:
        max_number = max(numeric_files, key=lambda x: x['number'])['number']

        # Passo 3: Filtrar arquivos com o maior número
        max_number_files = [f for f in numeric_files if f['number'] == max_number]

        # Passo 4: Filtrar o arquivo com o menor timestamp
        min_timestamp_file = min(max_number_files, key=lambda x: x['file']['createdTime'])

        return min_timestamp_file

    return numeric_files

def proof_of_work(previous_hash, name, drive, difficulty=4):
    nonce = random.uniform(1, 100)
    prefix = '0' * difficulty  # Exemplo: '0000' para dificuldade 4
    request = 50000

    while True:
        data = f"{previous_hash}{nonce}".encode()  # Concatena o hash anterior e o nonce
        new_hash = hashlib.sha256(data).hexdigest()  # Gera o hash
        

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

        nonce += 1  # Incrementa o nonce para tentar outro valor


def consensus_with_sleep_time(previous_hash):
    """
    Consenso baseado no tempo de espera (sleep time). O nó com o menor sleep time cria o bloco.
    
    previous_hash: O hash do bloco anterior.
    nodes: Lista de nós disponíveis para participar do consenso.
    
    Retorna o hash do novo bloco criado e o endereço do nó que o criou.
    """
    # Inicializar variáveis
    sleep_times = {}
    sleep_time_per_node = {}

    # Passo 1: Cada nó "dorme" por um tempo aleatório
    
    sleep_time = random.uniform(0.5, 10)  # Tempo de espera aleatório entre 0.5 e 3 segundos
    time.sleep(sleep_time)
    print(f"Nó {threading.current_thread().name} vai dormir por {sleep_time:.2f} segundos.")
    
    # Criar o novo bloco com o hash anterior e o endereço do nó selecionado
    data = f"{previous_hash}{previous_hash}".encode()
    new_hash = hashlib.sha256(data).hexdigest()

    print(f"PoS resolvido! Nó selecionado: {previous_hash}, Hash: {new_hash}")
    return new_hash

def get_numeric_files_level(files, level):
    out = []

    name = str(level)+".txt"

    for file in files:
        if (file['name'] == name):
            out.append(file)
    
    return out