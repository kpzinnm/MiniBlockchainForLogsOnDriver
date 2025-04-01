import re
import hashlib
import random

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
        # print(f)
        match = pattern.match(f['name'])
        if match:
            numeric_files.append({'file': f, 'number': int(match.group(1))})

    return numeric_files

def proof_of_work(previous_hash, difficulty=4):
    nonce = random.uniform(1, 100)
    prefix = '0' # Exemplo: '0000' para dificuldade 4

    while True:
        data = f"{previous_hash}{nonce}".encode()  # Concatena o hash anterior e o nonce
        new_hash = hashlib.sha256(data).hexdigest()  # Gera o hash

        if new_hash.startswith(prefix):
            print(f"PoW resolvido! Nonce: {nonce}, Hash: {new_hash}")
            return new_hash

        nonce += 1  # Incrementa o nonce para tentar outro valor
