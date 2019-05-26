import os
import time
from dotenv import load_dotenv
from instabot import Bot

timeout = 60
included_extensions = ['jpg','jpeg', 'tif', 'png', 'gif']
proxy = None

def get_image_dir():
    current_directory = os.path.dirname(__file__)
    return current_directory+'\\images'

def posting_images():

    load_dotenv()
    inta_user = os.getenv("instauser")
    insta_password = os.getenv("instapassword")

    image_directory = get_image_dir()
    file_names = os.listdir(image_directory)
      
    upload_images = [fn for fn in file_names
              if any(fn.endswith(ext) for ext in included_extensions)] 

    bot = Bot()
    bot.login(username=inta_user, password=insta_password, proxy=proxy)

    for upload_image in upload_images:
        if upload_image:
            file_path = f'{image_directory}\\{upload_image}'
            try:
                bot.upload_photo(file_path, caption=upload_image)
                if bot.api.last_response.status_code != 200:
                    print(bot.api.last_response)
            except Exception as error:
                print(str(error))
            
            time.sleep(timeout)