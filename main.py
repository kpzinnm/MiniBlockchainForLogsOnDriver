import threading
from drive_service import get_drive_service
from file_processor import get_largest_numbered_file, create_and_upload_new_file
from channels import Channels
# from test import run_benchmark

def process_drive_upload():
    """Função executada por cada thread para processar arquivos no Drive."""
    print("Thread Criada!")
    cont = 0
    while cont != 2:
        drive = get_drive_service()
        max_file = get_largest_numbered_file(drive)
        
        if max_file:
            retorno = create_and_upload_new_file(drive, max_file)
            if retorno == 0:
                cont += 0
            else:
                cont += 1

def run_blockchain():

    threads = []
    num_threads = 20

    for _ in range(num_threads):
        thread = threading.Thread(target=process_drive_upload)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Processo finalizado.")

    print("Precisamos encontrar a maior cadeia!!!!")

def search_channels():
    drive = get_drive_service()
    ch = Channels(drive)
    ch.make()

run_blockchain()
search_channels()

