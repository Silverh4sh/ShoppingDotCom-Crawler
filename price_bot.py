import scrapy
import json
from scrapy.crawler import CrawlerProcess

class PriceBot(scrapy.Spider):
	name = 'pricebot'
	query = 'Xbox'
	start_urls = ['http://www.shopping.com/'+query+'/products?CLT=SCH']

	def parse(self, response):

		prices_container = response.css('div:nth-child(2) > span:nth-child(1) > a:nth-child(1)')
		t_cont = response.css('div:nth-child(2)>h2:nth-child(1)>a:nth-child(1)>span:nth-child(1)')
			
		title = t_cont.xpath('@title').extract()
		price = prices_container.xpath('text()').extract()
		#Sanitise prices results
		prices = []
		for p in price:
			prices.append(p.strip('\n'))
		#Grouping Prices To Their Actual Products
		product_info = dict(zip(title, prices))
		with open('product_info.txt','w') as f:
			f.write(json.dumps(product_info))

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
def start_crawling():
	process.crawl(PriceBot)
	process.start()
start_crawling()
