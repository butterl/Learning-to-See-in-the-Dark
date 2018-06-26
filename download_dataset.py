import requests
import os
from os.path import exists, join, expanduser 

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    MB=100*1024*1024
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                size = size + 32768
                if size % MB == 0:
                    print("write: " + str(size/MB*100) + " MB")

if not exists("dataset/Sony.zip"):
    print('Dowloading Sony subset... (25GB)')
    download_file_from_google_drive('10kpAcvldtcb9G2ze5hTcF1odzu4V_Zvh', 'dataset/Sony.zip')
    os.system('unzip dataset/Sony.zip -d dataset')
#print('Dowloading Fuji subset... (52GB)')
#download_file_from_google_drive('12hvKCjwuilKTZPe9EZ7ZTb-azOmUA3HT', 'dataset/Fuji.zip')
#os.system('unzip dataset/Fuji.zip -d dataset')
