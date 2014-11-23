__author__ = 'xiayf'

import time

from pyquery import PyQuery as pq

from common import fetch_page, Storage, gen_fingerprint


class WangDaiZhiJiaParser(object):
    def __init__(self, config):
        self.config = config

    def __parse(self):

        result = []
        all_fingerprint = Storage.query_all_fingerprint(self.config['name'])

        url_list = [self.config['url'], ]
        while len(url_list):
            time.sleep(1)
            content = fetch_page(url_list.pop(len(url_list) - 1))
            if content is False:
                print 'Failed to fetch target page'
                return False
            dom_pq = pq(content)
            target_ele = dom_pq.find('#mod-answer-list')
            qa_list = target_ele.find('.bd').find('.cls-qa-table').find('table').find('tbody').find('tr').filter(lambda i: i > 0)
            for one_qa in qa_list:
                pq_qa = pq(one_qa)
                target_title_ele = pq_qa.children('td.title').find('.wrap').children('a')
                qa_href = target_title_ele.attr.href
                this_fingerprint = gen_fingerprint(qa_href)
                if this_fingerprint in all_fingerprint:
                    continue
                one_result = {
                    'name': self.config['name'],
                    'title': target_title_ele.attr.title,
                    'url': qa_href,
                    'fingerprint': this_fingerprint,
                    'created_time': pq_qa.children('td').eq(2).text()
                }
                all_fingerprint[this_fingerprint] = all_fingerprint.get(this_fingerprint, 0) + 1
                print one_result
                result.append(one_result)
            next_page = target_ele.find('.pages').find('a').filter('.n').eq(0)
            if len(next_page):
                url_list.append(next_page.attr.href)

        return result

    def run(self):
        results = self.__parse()
        Storage.add(results)