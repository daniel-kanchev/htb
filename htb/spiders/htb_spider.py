import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from htb.items import Article


class Htb_spiderSpider(scrapy.Spider):
    name = 'htb_spider'
    start_urls = ['https://www.htb.co.uk/news-and-insights/']

    def parse(self, response):
        links = response.xpath('//li[@class="mix third-flex-container news-insights-page-container'
                               ' latest-news tech "]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)


    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//section[@class="content"]/section[@class="content"][last()]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
