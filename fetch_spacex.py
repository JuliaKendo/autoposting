import logging
import requests
import os

FILENAME_TEMPLATE = 'spacex{0}.jpeg'
URL_TEMPLATE = 'https://api.spacexdata.com/v3/launches/latest'

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

def fetch_spacex_last_launch():
    
    responce = requests.get(URL_TEMPLATE)
    responce.raise_for_status()

    responce_json = responce.json()
    images_list = responce_json['links']['flickr_images']
    for num, image_url in enumerate(images_list):
        if image_url:
            image_name = FILENAME_TEMPLATE.format(num)
            logging.info(f'Загружаеться картинка: {image_name}')
            saved_filename = save_image(image_url, image_name)
            logging.info(f'Загружена картинка: {saved_filename}')
