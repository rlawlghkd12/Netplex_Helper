# -*- coding: utf-8 -*-
import scrapy
from test3.items import Test3Item

#justwatch홈페이지는 무한스크롤로 구현되어있어 내릴때 정보를 가져오는 곳을 찾아냄
base = 'https://apis.justwatch.com/content/titles/ko_KR/popular?body=%7B%22fields%22:[%22full_path%22,%22full_paths%22,%22id%22,%22localized_release_date%22,%22object_type%22,%22poster%22,%22scoring%22,%22title%22,%22tmdb_popularity%22,%22backdrops%22,%22production_countries%22,%22offers%22,%22original_release_year%22,%22backdrops%22],%22providers%22:[%22nfx%22],%22enable_provider_filter%22:false,%22is_upcoming%22:false,%22monetization_types%22:[],%22page%22:{0},%22page_size%22:100,%22matching_offers_only%22:true%7D&language=ko'
#^
#여기 page의 숫자를 바꾸면서 정보를 크롤링
domain = 'https://www.justwatch.com'
class Ex3Spider(scrapy.Spider):
    name = 'ex3.py'
    
    def start_requests(self):
        
        for i in range(1,21):
            yield scrapy.Request(url=base.format(i) , callback=self.parse_title)


    def parse_title(self, response):
        data = response.json()    
        for info in data['items']:
            path = info["offers"][0]['urls']['standard_web'] #넷플릭스 링크
            yield scrapy.Request(path , callback=self.parse_url)
    
                
    def parse_url(self, response):
        elink = response.url # 링크대로 들어가면 영어 버전으로 들어가진다.
        if '-en' in elink:
            link = elink.replace("-en","-kr")        #링크에 /kr-en에서 -en을 -kr로 바꾸거나 없애면 한글버전으로 불러온다
            yield scrapy.Request(link , callback=self.parse_info)
        
        
    def parse_info(self, response):
        item = Test3Item()
        item["title"] =response.xpath('//*[@id="section-hero"]/div[1]/div[1]/div[2]/div/h1/text()').extract()[0] #제목
        genre = response.xpath('//*[@id="section-more-details"]/div[2]/div[1]/div[1]/text()').extract()#장르
        if '장르' in genre:
            #오프라인 저장 컨텐츠 다음 장르가 오는 경우
            genres_list=response.xpath('//*[@id="section-more-details"]/div[2]/div[1]/div[2]/span/a/text()').extract()
        else: 
            #오프라인 저장 컨텐츠 없이 바로 장르가 오는 경우
            genres_list=response.xpath('//*[@id="section-more-details"]/div[2]/div[2]/div[2]/span/a/text()').extract()#장르
            if not genres_list:
                #장르 경로가 /a/text()가 아닌 바로 text()
                genres_list = response.xpath('//*[@id="section-more-details"]/div[2]/div[2]/div[2]/span/text()').extract()
        item["genres"]=' '.join(genres_list)#장르가 리스트 형식으로 오기때문에 문자열 형식으로 바꾸어 준다
        item["link"] = response.url #넷플릭스 링크
        yield item
        

        
       