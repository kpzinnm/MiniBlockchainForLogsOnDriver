import re

def get_numeric_files(files):
    """
    Filtra arquivos cujos nomes começam com um número seguido de uma extensão.
    
    Retorna uma lista de dicionários, onde cada dicionário contém:
    - 'file': o arquivo original
    - 'number': a parte numérica extraída do nome
    """
    numeric_files = []
    pattern = re.compile(r"^(\d+)\..+$")  # Captura apenas arquivos no formato número.extensão

    for f in files:
        print(f)
        match = pattern.match(f['name'])
        if match:
            numeric_files.append({'file': f, 'number': int(match.group(1))})

    return numeric_files
