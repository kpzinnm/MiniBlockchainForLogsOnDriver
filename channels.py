from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

def get_files(drive):
    
    files = drive.files().list().execute().get('files', [])
    
    print(files)