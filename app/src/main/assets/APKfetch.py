#!/usr/bin/python
from __future__ import print_function
from bs4 import BeautifulSoup
import json
import requests

url = "http://www.androidapksfree.com/apk/youtube-apk-latest-version-download/"

json_file = open('HookClassnames.json').read()

# key_val_pair requires a dictionary from youtube.py HookExtractor


def process(key_val_pair):
    key = ""
    val = ""
    for k in key_val_pair:
        key, val = k, key_val_pair[k]

    app = APKFetch(url)  # Printable print(app)
    app_url = app['url']
    app_version = app['version']
    app_found = app['found']

    print(app_url)

    if(app_found == 0):
        json_data = json.loads(json_file)
        json_data['Youtube'][str(app_version)] = dict()
        # Key_val pair changes later
        json_data['Youtube'][str(app_version)][key] = val
        with open('HookClassnames.json', 'wb+') as f:
            json.dump(json_data, f, sort_keys=True, indent=4)
        print("HookClassnames.json Updated with " + str(app_version))
        f.close()
    else:
        print ("Found")


def APKFetch(url):
    result = {}
    data = requests.get(url).text

    soup = BeautifulSoup(data, "html.parser")
    links = soup.find_all('a')

    for link in links:
        x = link.get('href')
        if('com.google.android.youtube_' in x):
            result['url'] = x
            break

    title = soup.title.text.split()
    version = title[2].zfill(6)[1:7]

    result['version'] = int(version)
    result['found'] = jsonCheck(version)

    return result


def jsonCheck(version):
    json_data = json.loads(json_file)
    youtube = json_data['Youtube']
    if (str(version) not in youtube):
        return 0
    else:
        return 1
    json_file.close()
