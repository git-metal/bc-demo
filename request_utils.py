# -*- coding:utf-8 -*-

import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def get(url):
    return requests.get(url,  headers=headers)


def get_html(url):
    print(f"url:{url}")
    response = requests.get(url, headers=headers)
    # return response.content.decode()
    return response.text

def download_img(url):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        return None