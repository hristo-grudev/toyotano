import scrapy

from scrapy.loader import ItemLoader
from ..items import ToyotanoItem
from itemloaders.processors import TakeFirst


class ToyotanoSpider(scrapy.Spider):
	name = 'toyotano'
	start_urls = ['https://www.toyota.no/world-of-toyota/index.json']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class, "element")]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()[normalize-space()]|//center/h2/text()').get()
		description = response.xpath('//article[@id="article-v2"]//text()[normalize-space()]|//article[@class="section"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=ToyotanoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
