import requests
import fetch_spacex
import fetch_hubble
import posting_images

if __name__ == "__main__":
    
    try:
        fetch_spacex.fetch_spacex_last_launch() 
    except requests.exceptions.HTTPError as error:
        print("Не могу получить данные с сервера Space X:\n{0}".format(error))
    
    try:
        fetch_hubble.fetch_hubble_images()  
    except requests.exceptions.HTTPError as error:
        print("Не могу получить данные с сервера habble:\n{0}".format(error))

    posting_images.posting_images()