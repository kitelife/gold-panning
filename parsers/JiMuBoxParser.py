# coding: utf-8

__author__ = 'xiayf'

import time

from pyquery import PyQuery as pq

from common import fetch_page, Storage, ParserBase, gen_fingerprint


class JiMuBoxParser(ParserBase):

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
            target_father = dom_pq.find('div.main_content')
            # 取帖子
            target_qa_td = target_father.find('div.thread_posts_list').children('table#J_posts_list').find('td.subject')
            for tqt in target_qa_td:
                pq_tqt = pq(tqt)
                target_title_ele = pq_tqt.children('p.title').find('a.st').eq(1)
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
                    'created_time': pq_tqt.children('p.info').children('span').eq(0).text()
                }
                self.all_fingerprint[this_fingerprint] = 1
                print one_result
                result.append(one_result)
            # 取下一页的地址
            next_page_a = target_father.find('div.J_page_wrap').eq(1).children('.pages').children('a.pages_next')
            if next_page_a:
                self.url_list.append(next_page_a.attr.href)
                print self.url_list

        return result

    def run(self):
        result = self.__parse()
        Storage.add(result)