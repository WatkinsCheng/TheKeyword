# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ThekeywordPipeline(object):
    def __init__(self):
        self.f = open("thekeyword_pipeline.json", "wb+")

    def process_item(self, item, spider):
        # 将数据强制转换成字典
        if item:
            content = json.dumps(dict(item), ensure_ascii=False)+'\n'
            self.f.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.f.close()