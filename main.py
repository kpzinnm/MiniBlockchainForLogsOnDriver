import threading
from drive_service import get_drive_service
from file_processor import get_largest_numbered_file, create_and_upload_new_file

def process_drive_upload():
    """Função executada por cada thread para processar arquivos no Drive."""
    print("Thread Criada!")
    cont = 0
    while cont != 5:
        drive = get_drive_service()
        max_file = get_largest_numbered_file(drive)
        
        if max_file:
            create_and_upload_new_file(drive, max_file)
        cont += 1

# Criando múltiplas threads para execução simultânea
threads = []
num_threads = 30  # Número de threads para rodar em paralelo

for _ in range(num_threads):
    thread = threading.Thread(target=process_drive_upload)
    threads.append(thread)
    thread.start()

# Aguarda todas as threads finalizarem
for thread in threads:
    thread.join()

print("Processo finalizado.")

print("Precisamos encontrar a maior cadeia!!!!")
