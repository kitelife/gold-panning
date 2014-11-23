# coding: utf-8

__author__ = 'xiayf'

import sys

import multiprocessing

from parsers import *

CONFIGS = [
    {
        'name': u'网贷之家 - 问答',
        'url': 'http://www.wangdaizhijia.com/wenda/c-all/all/',
        'parser': WangDaiZhiJiaParser,
    },
]


class Crawler(object):

    @classmethod
    def run(cls):
        process_records = []
        for config in CONFIGS:
            parser_class = config.pop('parser')
            target_parser = parser_class(config)
            new_process = multiprocessing.Process(target=target_parser.run)
            new_process.start()
            process_records.append(new_process)

        for pr in process_records:
            pr.join()


if __name__ == '__main__':
    Crawler.run()