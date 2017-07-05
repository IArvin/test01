# -*-coding: utf-8-*-
# !usr/bin/python
import logging
from logging.handlers import TimedRotatingFileHandler
import requests
import json
import time
from pyquery import PyQuery as pq
import sys

# createTime: 2017-07-05 12:30:36
# desc: bt0 website

reload(sys)
sys.setdefaultencoding('utf-8')


def config_log():
    level = logging.INFO
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('BT0Scrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d.log"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=level, format=fmt)
    log.addHandler(fileTimeHandler)


class BT0Scrapy():
    def __init__(self):
        self.session = requests.session()
        self.timeout = 15

    def main(self):
        self.requestSelectPage()

    def requestSelectPage(self):
        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        self.session.headers['Accept-Encoding'] = 'gzip, deflate, sdch'
        self.session.headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        self.session.headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        resources_all = self.session.get('http://www.bt0.com/film-download/1-0-0-0-0-0.html', verify=False,
                                         timeout=self.timeout)
        b = pq(resources_all.content.encode('utf-8'))
        get_pageNums = b('ul[class="tsc_pagination tsc_paginationA tsc_paginationA06"] li')
        page_nums = None
        for nums in get_pageNums:
            judge = b('li', nums).text()
            if '.' in judge:
                page_nums = judge.replace('.', '')
        for x in xrange(0, int(page_nums)):
            new_page = self.session.get('http://www.bt0.com/film-download/1-0-0-0-0-%s.html' % str(x),
                                        timeout=self.timeout)
            b = pq(new_page.content)
            movie_detail_list = self.movie_detail(b)
            for movie in movie_detail_list:
                response = self.session.get(movie['movie_url'], timeout=self.timeout)
                b = pq(response.content)
                magnetic_link_list = b('div[class="picture-container"] div[class="container"]')
                link_list = []
                for link in magnetic_link_list:
                    magnetic_link = b('div[class="container"] div:eq(3) a', link).attr('href')
                    link_list.append(magnetic_link)
                movie['link_list'] = link_list
            print json.dumps(movie_detail_list)

    def movie_detail(self, b):
        div_list = b('div[class="masonry__container"] div')
        type_list = [u'又名:', u'类型:', u'片长:', u'上映地区:']
        detail_list = []
        for div in div_list:
            detail_dict = {}
            detail_dict['image'] = b('img', div).attr('src')
            detail_dict['movie_name'] = b('img', div).attr('alt')
            movie_msg = b('p', div).text().split(' ')
            detail_dict['movie_url'] = 'http://www.bt0.com' + b('a', div).attr('href')
            detail_dict['origin_year'] = b('h2', div).text().split(' ')[-1]
            new_name = ''
            for index, mov_msg in enumerate(movie_msg):
                if u'又名:' in mov_msg:
                    if ':' not in movie_msg[index + 1]:
                        detail_dict['new_name'] = movie_msg[index + 1]
                    if ':' in movie_msg[index + 1] and movie_msg[index + 1] not in type_list:
                        for x in xrange(index + 1, len(movie_msg)):
                            if movie_msg[index + x] in type_list:
                                break
                            detail_dict['new_name'] = new_name + movie_msg[index + x]
                elif u'类型:' in mov_msg:
                    detail_dict['movie_type'] = movie_msg[index + 1] = movie_msg[index + 1]
                elif u'片长:' in mov_msg:
                    detail_dict['movie_time'] = movie_msg[index + 1]
                elif u'上映地区:' in mov_msg:
                    detail_dict['origin'] = movie_msg[index + 1]
            detail_list.append(detail_dict)
        return detail_list


if __name__ == '__main__':
    config_log()
    scrapy = BT0Scrapy()
    scrapy.main()
