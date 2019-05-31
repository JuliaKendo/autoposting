import logging
import requests
import os
import fetch_spacex
import fetch_hubble
import posting_images

def main():
    
    current_directory = os.path.dirname(__file__)
    logfile = os.path.join(current_directory,'autoposting.log')   
    logging.basicConfig(filename=logfile, filemode='w')
    logging.info("Program started")
    
    try:
        fetch_spacex.fetch_spacex_last_launch() 
    except requests.exceptions.HTTPError as error:
        logging.info("Не могу получить данные с сервера Space X:\n{0}".format(error))
    
    try:
        fetch_hubble.fetch_hubble_images()  
    except requests.exceptions.HTTPError as error:
        logging.info("Не могу получить данные с сервера habble:\n{0}".format(error))

    posting_images.posting_images()

    logging.info("Done!")

if __name__ == "__main__":
    main()
    
