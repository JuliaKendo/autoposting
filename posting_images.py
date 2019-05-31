import os
import time
import logging
from dotenv import load_dotenv
from instabot import Bot

TIMEOUT = 60
INCLUDED_EXTENSIONS = ['jpg','jpeg', 'tif', 'png', 'gif']
PROXY = None

def get_image_directory():
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory,'images')

def posting_images():

    load_dotenv()
    inta_user = os.getenv("instauser")
    insta_password = os.getenv("instapassword")

    image_directory = get_image_directory()
    file_names = os.listdir(image_directory)
      
    upload_images = [fn for fn in file_names
              if any(fn.endswith(ext) for ext in INCLUDED_EXTENSIONS)] 

    bot = Bot()
    bot.login(username=inta_user, password=insta_password, proxy=PROXY)

    for upload_image in upload_images:
        if upload_image:
            file_path = os.path.join(image_directory,upload_image)
            try:
                bot.upload_photo(file_path, caption=upload_image)
                if bot.api.last_response.status_code != 200:
                    logging.error(bot.api.last_response)
            except Exception as error:
                logging.error("Ошибка загрузки фото в инстаграмм: {}".format(error))
            
            time.sleep(TIMEOUT)