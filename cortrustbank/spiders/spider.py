import scrapy

from scrapy.loader import ItemLoader

from ..items import CortrustbankItem
from itemloaders.processors import TakeFirst


class CortrustbankSpider(scrapy.Spider):
	name = 'cortrustbank'
	start_urls = ['https://www.cortrustbank.com/news']

	def parse(self, response):
		post_links = response.xpath('//section[@class="l-page__primary"]//article/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//nav[@class="pagination"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="sub-header__title"]/text()').get()
		description = response.xpath('//section[@class="l-page__primary"]//div[@class="wysiwyg"][1]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=CortrustbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
