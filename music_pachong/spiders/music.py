import scrapy
from music_pachong.items.SongType import SongItem


class ZzSpider(scrapy.Spider):
    name = "music"
    allowed_domains = []
    start_urls = [
        "http://www.migu.cn/search.html?content=%E5%91%A8%E6%9D%B0%E4%BC%A6&type=music&_ch="
    ]

    def parse(self, response):
        pages = response.xpath("//div[@class='pagination text-right']/ul/li[6]/a/text()").extract_first()
        pages = int(pages)
        for page in range(pages):
            pn = str(page + 1)
            yield scrapy.Request(
                url="http://www.migu.cn/search.html?content=%E5%91%A8%E6%9D%B0%E4%BC%A6&type=music&pn=" + pn,
                callback=self.song)

    def song(self, response):
        options = response.xpath("//div[@class='list']/ul/li")
        for option in options:
            name = option.xpath(".//a/div[@class='info']/h3/span[2]/text()").extract_first()
            href = option.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url=href, callback=self.sing, meta={'name': name})

    def sing(self, response):
        type = response.xpath("//div[@class='info_about']/p[4]/span/span/text()").extract()
        name = response.meta['name']
        item = SongItem()
        item['name'] = name
        item['type'] = type
        yield item
