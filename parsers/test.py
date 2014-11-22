__author__ = 'xiayf'

from common import fetch_page


class TestParser(object):

    def __init__(self, configs):
        self.configs = configs

    def parse(self):
        print fetch_page(self.configs['url'])