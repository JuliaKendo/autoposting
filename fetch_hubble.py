import requests
import os

url_template = 'http://hubblesite.org/api/v3/image/{}'
image_collections = ["all","holiday_cards","wallpaper","spacecraft","news","printshop","stsci_gallery"]

def get_image_dir():
    current_directory = os.path.dirname(__file__)
    return current_directory+'\\images'

def save_image(url, filename):
    image_directory = get_image_dir()
    file_path = f'{image_directory}\\{filename}'

    if not os.path.exists(image_directory):
        os.mkdir(image_directory)

    responce = requests.get(url)
    responce.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(responce.content)

    return file_path

def get_file_extention(file_path):
    if not file_path:
        return None

    lst = file_path.split('.')
    return lst[len(lst)-1]

def get_hubbl_id_images(url):
    
    list_id = []
    responce = requests.get(url)
    responce.raise_for_status()

    responce_json = responce.json()
    for item in responce_json:
        list_id.append(item['id'])
   
    return list_id 

def get_hablle_url(image_files):
    i=len(image_files)-1
    while i>0:
        image_line = image_files[i]
        file_size = image_line['file_size']
        if file_size <= 20000000:
            return image_line['file_url']
        i=i-1
        
    image_line = image_files[len(image_files)-1]
    return image_line['file_url']
    
def get_hubble_images(url):

    images_id = get_hubbl_id_images(url)
    for image_id in images_id:
        responce = requests.get(url_template.format(image_id))
        responce.raise_for_status()

        responce_json = responce.json()
        image_files = responce_json['image_files']
        image_url = get_hablle_url(image_files)
        image_name = "{0}.{1}".format(str(image_id), get_file_extention(image_url))
        print(f'Загружаеться картинка: {image_name}')
        saved_filename = save_image(image_url, image_name)
        print(f'Загружена картинка: {saved_filename}')


def fetch_hubble_images():
        
    for image_collection in image_collections:
        url = url_template.format(image_collection)
        get_hubble_images(url)
