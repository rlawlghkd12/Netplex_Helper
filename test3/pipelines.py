# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Test3Pipeline(object):
    def __init__(self):
        self.csvwriter = csv.writer(open("netflixinfo.csv","w", newline=""))
        self.csvwriter.writerow(["title","genres","link"])
        #self.rowcount =1
        
    def process_item(self, item, spider):
        #self.csvwriter.writerow('A%s' % self.rowcount, item.get('title'))
        #self.csvwriter.writerow('A%s' % self.rowcount, item.get('genres'))
        #self.csvwriter.writerow('A%s' % self.rowcount, item.get('link'))
        #self.rowcount += 1
        row = []
        row.append(item["title"])
        row.append(item["genres"])
        row.append(item["link"])
        self.csvwriter.writerow(row)
        return item
