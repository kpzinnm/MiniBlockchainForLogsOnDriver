from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from utils import get_numeric_files_level, get_numeric_files
import io
import json
from googleapiclient.errors import HttpError

class Channels():

    def __init__(self, drive):
        self.drive = drive

    def make(self):
        head = True

        branches = []

        while (True):
            if (head):
                head_block = self.get_head()
                position_in_chain = 0
                level = head_block['number']
                self.favorite_files(head_block['file']['id'])
                blockDic = self.download_block(head_block['file']['id'])
                blockDic['id'] = head_block['file']['id']
                branches.append(blockDic)
                while (level >= 0):
                    level -= 1
                    blocks_level = self.get_files_level(level)
                    blocksTMP = []
                    print(blocks_level)
                    for i in blocks_level:
                        print("BLOCO PROCESSADO: ")
                        print(i)
                        blockDic_TMP = self.download_block(i['id'])
                        blockDic_TMP['id'] = i['id']
                        blocksTMP.append(blockDic_TMP)
                        print("saiu do IF:")

                    hash_goal = branches[position_in_chain]['previous_hash']
                    print(hash_goal)
                    for i in blocksTMP:
                        print("VERIFICAÇÃO DE HASH: ")
                        print(i)
                        if (i['hash'] == hash_goal):
                            print("Adicionei:")
                            print(i)
                            self.favorite_files(i['id'])
                            branches.append(i)
                            position_in_chain += 1
                            break
                print(branches)
                self.save_chan_one(branches)
                break
                   
    def save_chan_one(self, chan):
        with open("chan01.txt", "w") as file:
            json.dump(chan, file, indent=4)


    def download_block(self, id):
        request = self.drive.files().get_media(fileId=id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False    
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)
        content = file_stream.read().decode("utf-8")  

        contentDict = json.loads(content)
        return contentDict

    def favorite_files(self, file_id):
        print(f"Favoritando arquivo: {file_id}")

        try:
            self.drive.files().update(  
                fileId=file_id,
                body={"starred": True}
            ).execute()
            print(f"Arquivo {file_id} favoritado com sucesso!")
        except HttpError as error:
            print(f"Erro ao favoritar arquivo {file_id}: {error}")

    def get_files_level(self, level):
        
        files = self.drive.files().list().execute().get('files', [])

        return get_numeric_files_level(files, int(level))

    def get_head(self):
        head = self.drive.files().list(
            pageSize=10,  
            fields="files(id, name, createdTime)",
            orderBy="createdTime desc"  
        ).execute().get('files', [])
        print("TODOS OS ARQUIVOS HEADD!!!!!!!!!!!!!!!!")
        print(head)
        head_block = get_numeric_files(head)

        return head_block