import logging
import requests
import os

MAX_SIZE_IMAGE = 20000000
URL_TEMPLATE = 'http://hubblesite.org/api/v3/image/{}'
IMAGE_COLLECTIONS = ["all","holiday_cards","wallpaper","spacecraft","news","printshop","stsci_gallery"]

def get_image_directory():
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory,'images')

def save_image(url, filename):
    image_directory = get_image_directory()    
    file_path = os.path.join(image_directory,filename) 
    os.makedirs(image_directory, exist_ok=True)

    responce = requests.get(url)
    responce.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(responce.content)

    return file_path

def get_file_extention(file_path):
    if not file_path:
        return None

    splited_file_path = file_path.split('.')
    return splited_file_path[len(splited_file_path)-1]

def get_hubble_images_id(url):
    
    list_id = []
    responce = requests.get(url)
    responce.raise_for_status()

    responce_json = responce.json()
    for item in responce_json:
        list_id.append(item['id'])
   
    return list_id 

def get_hublle_url(image_files):
    for number_line in range(len(image_files)-1,-1,-1):
        image_line = image_files[number_line]
        file_size = image_line['file_size']
        if file_size <= MAX_SIZE_IMAGE:
            return image_line['file_url']
        
    image_line = image_files[len(image_files)-1]
    return image_line['file_url']
    
def get_hubble_images(url):

    images_id = get_hubble_images_id(url)
    for image_id in images_id:
        responce = requests.get(URL_TEMPLATE.format(image_id))
        responce.raise_for_status()

        responce_json = responce.json()
        image_files = responce_json['image_files']
        image_url = get_hublle_url(image_files)
        image_name = "{0}.{1}".format(str(image_id), get_file_extention(image_url))
        logging.info(f'Загружаеться картинка: {image_name}')
        saved_filename = save_image(image_url, image_name)
        logging.info(f'Загружена картинка: {saved_filename}')


def fetch_hubble_images():
        
    for image_collection in IMAGE_COLLECTIONS:
        url = URL_TEMPLATE.format(image_collection)
        get_hubble_images(url)
