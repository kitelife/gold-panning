__author__ = 'xiayf'

import requests


def fetch_page(url):
    r = requests.get(url)
    if r.status_code != 200:
        return False
    return r.text