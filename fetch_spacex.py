import requests
import os

filename_template = 'spacex{0}.jpeg'
url_template = 'https://api.spacexdata.com/v3/launches/latest'

def get_image_dir():
    current_directory = os.path.dirname(__file__)
    return current_directory+'\images'

def save_image(url, filename):
    image_directory = get_image_dir()
    file_path = f'{image_directory}\{filename}'

    if not os.path.exists(image_directory):
        os.mkdir(image_directory)

    responce = requests.get(url)
    responce.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(responce.content)

    return file_path

def fetch_spacex_last_launch():
    
    responce = requests.get(url_template)
    responce.raise_for_status()

    responce_json = responce.json()
    images_list = responce_json['links']['flickr_images']
    for num, image_url in enumerate(images_list):
        if image_url:
            image_name = filename_template.format(num)
            print(f'Загружаеться картинка: {image_name}')
            saved_filename = save_image(image_url, image_name)
            print(f'Загружена картинка: {saved_filename}')
