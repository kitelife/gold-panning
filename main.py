# coding: utf-8

__author__ = 'xiayf'

import multiprocessing

from parsers import *

CONFIGS = [
    {
        'url': 'http://www.baidu.com',
        'parser': TestParser,
    },
    {
        'url': 'http://ce.baidu.com',
        'parser': TestParser,
    },
]


class Crawler(object):

    @classmethod
    def run(cls):
        process_records = []
        for config in CONFIGS:
            parser_class = config.pop('parser')
            target_parser = parser_class(config)
            new_process = multiprocessing.Process(target=target_parser.parse)
            new_process.start()
            process_records.append(new_process)

        for pr in process_records:
            pr.join()


if __name__ == '__main__':
    Crawler.run()