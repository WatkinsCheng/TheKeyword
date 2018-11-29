# -*- coding: utf-8 -*-
import scrapy
import re
from TheKeyword.items import ThekeywordItem


class ThesentenceSpider(scrapy.Spider):
    # 定义一个名为thesentence的爬虫
    name = 'thesentence'
    # 允许爬虫域的范围
    # carmagazine.co.uk /
    allowed_domains = ['en.wikipedia.org']
    # 爬虫执行后第一批请求从该表中获取
    start_urls = ['https://en.wikipedia.org/wiki/Car']
    # 下载延时
    # download_delay = 1

    def parse(self, response):
        # 获取div标签里面所有文本
        node_list = response.xpath("//p")
        for node in node_list:
            # 创建item字段对象，用来存储信息
            item = ThekeywordItem()
            # 去掉标签和空格换行符,不区分大小写
            # delete_lable = re.compile(r'\t|\n|', re.S)
            # item['info'] = delete_lable.sub('', content)
            # info = node.xpath('normalize-space(string(.))').extract()
            # xpath时候匹配到空值会出现 IndexError: list index out of range
            # item['info'] = info[0] if info else None
            p = node.xpath('normalize-space(string(.))').extract()
            item['p'] = p[0] if p else None
            # 返回提取到的每个item数据，给管道文件，并返回来继续执行后面的代码
            yield item





