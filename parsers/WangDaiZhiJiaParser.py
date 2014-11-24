# coding: utf-8

__author__ = 'xiayf'

import time

from pyquery import PyQuery as pq

from common import fetch_page, Storage, ParserBase, gen_fingerprint


class WangDaiZhiJiaParser(ParserBase):

    def __init__(self, config):
        ParserBase.__init__(self, config)

    def __parse(self):
        result = []
        while len(self.url_list):
            time.sleep(2)
            content = fetch_page(self.url_list.pop())
            if content is False:
                print 'Failed to fetch target page'
                return False
            dom_pq = pq(content)
            target_ele = dom_pq.find('#mod-answer-list')
            qa_list = target_ele.find('.bd').find('.cls-qa-table').find('table').find('tbody').find('tr').filter(
                lambda i: i > 0)
            for one_qa in qa_list:
                pq_qa = pq(one_qa)
                target_title_ele = pq_qa.children('td.title').find('.wrap').children('a')
                qa_href = target_title_ele.attr.href
                this_fingerprint = gen_fingerprint(qa_href)
                if this_fingerprint in self.all_fingerprint:
                    self.has_duplicate = True
                    # 一旦出现重复，就没必要继续了
                    break
                one_result = {
                    'name': self.config['name'],
                    'title': target_title_ele.attr.title,
                    'url': qa_href,
                    'fingerprint': this_fingerprint,
                    'created_time': pq_qa.children('td').eq(2).text()
                }
                self.all_fingerprint[this_fingerprint] = 1
                print one_result
                result.append(one_result)

            if self.has_duplicate:
                print self.config['name'], 'finished!'
                break
            maybe_next_page = target_ele.find('.pages').find('a').filter('.n')
            for np in maybe_next_page:
                pq_np = pq(np)
                if pq_np.text() == u'下一页':
                    self.url_list.append(pq_np.attr.href)
                    print self.url_list

        return result

    def run(self):
        result = self.__parse()
        Storage.add(result)