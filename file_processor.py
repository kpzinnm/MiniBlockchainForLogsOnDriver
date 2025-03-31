import os
from googleapiclient.http import MediaFileUpload
from utils import get_numeric_files

def get_largest_numbered_file(drive):
    """Encontra o arquivo com o maior número no nome e retorna seus metadados."""
    files = drive.files().list().execute().get('files', [])
    numeric_files = get_numeric_files(files)

    if not numeric_files:
        print("Nenhum arquivo numérico encontrado.")
        return None

    # Encontra o arquivo com o maior número
    max_file_data = max(numeric_files, key=lambda f: f['number'])
    return max_file_data['number']  # Retorna o arquivo original

def create_and_upload_new_file(drive, max_file):
    """Cria um novo arquivo com um número maior e faz upload para o Google Drive."""
    max_number = max_file
    new_number = max_number + 1
    new_file_name = f"{new_number}"

    # file_metadata = drive.files().get(fileId=max_file['id']).execute()
    # mime_type = file_metadata.get('mimeType')

    temp_file_path = f"{new_file_name}.txt"
    with open(temp_file_path, "w") as f:
        f.write(f"Arquivo gerado com número {new_number}")

    media = MediaFileUpload(temp_file_path, mimetype='text/plain')
    
    new_metadata = {'name': temp_file_path, 'mimeType': 'text/plain'}
    uploaded_file = drive.files().create(body=new_metadata, media_body=media, fields='id').execute()
    
    print(f"Novo arquivo enviado: {new_file_name} (ID: {uploaded_file['id']})")
    
    os.remove(temp_file_path) #Condição de corrida, so a primeira thread deveria excluir o arquivo
