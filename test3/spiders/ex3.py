# -*- coding: utf-8 -*-
import scrapy
from test3.items import Test3Item
base = 'https://apis.justwatch.com/content/titles/ko_KR/popular?body=%7B%22fields%22:[%22full_path%22,%22full_paths%22,%22id%22,%22localized_release_date%22,%22object_type%22,%22poster%22,%22scoring%22,%22title%22,%22tmdb_popularity%22,%22backdrops%22,%22production_countries%22,%22offers%22,%22original_release_year%22,%22backdrops%22],%22providers%22:[%22nfx%22],%22enable_provider_filter%22:false,%22is_upcoming%22:false,%22monetization_types%22:[],%22page%22:{0},%22page_size%22:100,%22matching_offers_only%22:true%7D&language=ko'

domain = 'https://www.justwatch.com'
class Ex3Spider(scrapy.Spider):
    name = 'ex3.py'
   
    def start_requests(self):
        for i in range(1,21):
            yield scrapy.Request(url=base.format(i) , callback=self.parse_title)

    def parse_title(self, response):
        data = response.json()
        for info in data['items']:
            path = info["full_path"]
            url = domain+path
            yield scrapy.Request(url , callback=self.parse_nlink)
    
    def parse_nlink(self, response):
        nlink1= response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/a/@href').extract()[0]
        if 'www.netflix.com' in nlink1:
            yield scrapy.Request(nlink1 , callback=self.parse_url)
        #넷플릭스이외인경우
        else: 
            nlink2 = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/a/@href').extract()[0]
            if 'www.netflix.com' in nlink2:
                yield scrapy.Request(nlink2 , callback=self.parse_url)
            else: 
                nlink3 = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div[3]/div/a/@href').extract()[0]
                if 'netflix' in nlink:
                    yield scrapy.Request(nlink3 , callback=self.parse_url)
                else: return 0
                
    def parse_url(self, response):
        elink = response.url # english version
        if '-en' in elink:
            link = elink.replace("-en","")        #링크가 kr-en에서  -en을 빼면 한국버전
            yield scrapy.Request(link , callback=self.parse_info)
        else: pass
        

    def parse_info(self, response):
        item = Test3Item()
        item["title"] =response.xpath('//*[@id="section-hero"]/div[1]/div[1]/div[2]/div/h1/text()').extract()
        genres_list=response.xpath('//*[@id="section-more-details"]/div[2]/div[2]/div[2]/span/a/text()').extract()
        item["genres"]=' '.join(genres_list)
        item["link"] = response.url
        yield item
        

        
       