#!/usr/bin/env python3

import os
import sys
import json
from gphotospy import authorize
from gphotospy.album import *
from gphotospy.media import *
from datetime import date as dt
import requests
from pprint import pprint



def get_service(my_secret_file_name):
    CLIENT_SECRET_FILE = my_secret_file_name
    service = authorize.init(CLIENT_SECRET_FILE)
    return service


def download_file(url, destination_folder, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        print('Downloading file {0}'.format(file_name))
        with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)
            f.close()


def get_medias(service, media_iterator, medias):
    try:
        file = {}
        data = json.dumps(next(media_iterator), indent=5)
        data = json.loads(data)
        file["name"] = data["filename"]
        file["url"] = data["baseUrl"]
        medias.append(file)
        get_medias(service, media_iterator, medias)
    except (StopIteration, TypeError) as e:
        return


def get_today_media(service):
    today = dt.today()
    medias = []
    media_manager = Media(service)
    media_iterator = media_manager.search(
        filter=[date(today.year, today.month, today.day)])
    # media_iterator = media_manager.search(filter=[date(2022, 1, 9)])
    get_medias(service, media_iterator, medias)
    return medias


def main():
    if len(sys.argv) != 3:
        sys.exit(84)
    my_secret_file_name = sys.argv[1]
    save_folder = sys.argv[2]
    service = get_service(my_secret_file_name)
    medias = get_today_media(service)
    for it in medias:
        download_file(it["url"] + "=d", save_folder, it["name"])


if __name__ == "__main__":
    main()
