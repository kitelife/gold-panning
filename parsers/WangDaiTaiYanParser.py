# coding: utf-8

__author__ = 'xiayf'

import time

from pyquery import PyQuery as pq

from common import fetch_page, Storage, ParserBase, gen_fingerprint


class WangDaiTianYanParser(ParserBase):

    def __init__(self, config):
        ParserBase.__init__(self, config)

    def __parse(self):
        result = []
        last_page_num = -1
        next_page_num = 1
        while len(self.url_list):
            time.sleep(2)
            content = fetch_page(self.url_list.pop())
            if content is False:
                print 'Failed to fetch target page'
                return False
            dom_pq = pq(content)
            target_father = dom_pq.find('.cls-qa-table')
            # 取当前页问题列表
            target_qa_trs = target_father.children('table').find('tr').filter(lambda i: i % 2 == 1)
            for qa_tr in target_qa_trs:
                pq_qa = pq(qa_tr)
                target_qa_item = pq_qa.find('.titlee').find('a.lnk')
                qa_href = target_qa_item.attr.href
                print qa_href
                this_fingerprint = gen_fingerprint(qa_href)
                if this_fingerprint in self.all_fingerprint:
                    self.has_duplicate = True
                    break
                one_result = {
                    'name': self.config['name'],
                    'title': target_qa_item.attr.title,
                    'url': qa_href,
                    'fingerprint': this_fingerprint,
                    'created_time': pq_qa.find('td').eq(2).text()
                }
                result.append(one_result)
                print one_result

            if self.has_duplicate:
                break
            # 取下一页的地址
            if last_page_num == -1:
                last_page_href = target_father.find('div.pg').find('a.last').attr.href
                last_page_num = int(last_page_href.split('/')[-1])
            if next_page_num < last_page_num-1:
                next_page_num += 1
                self.url_list.append('http://www.p2peye.com/ask/a2/' + str(next_page_num))
                print self.url_list
        return result

    def run(self):
        result = self.__parse()
        Storage.add(result)