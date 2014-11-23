__author__ = 'xiayf'

import time

from pyquery import PyQuery as pq

from common import fetch_page


class WangDaiZhiJiaParser(object):
    def __init__(self, config):
        self.config = config

    def __parse(self):

        result = []

        def inner_parser(url):
            content = fetch_page(url)
            if content is False:
                print 'Failed to fetch target page'
                return False
            dom_pq = pq(content)
            target_ele = dom_pq.find('#mod-answer-list')
            qa_list = target_ele.find('.bd').find('.cls-qa-table').find('table').find('tbody').find('tr').filter(lambda i: i > 0)
            for one_qa in qa_list:
                one_result = {}
                pq_qa = pq(one_qa)
                target_title_ele = pq_qa.children('td.title').find('.wrap').children('a')
                one_result['href'] = target_title_ele.attr.href
                one_result['title'] = target_title_ele.attr.title
                one_result['created_time'] = pq_qa.children('td').eq(2).text()
                print one_result
                result.append(one_result)
            next_page = target_ele.find('.pages').find('a').filter('.n').eq(0)
            if len(next_page):
                time.sleep(1)
                inner_parser(next_page.attr.href)

        inner_parser(self.config['url'])

        return result

    def __store(self, results):
        pass

    def run(self):
        results = self.__parse()
        self.__store(results)