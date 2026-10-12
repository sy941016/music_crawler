import scrapy
from urllib.parse import quote
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from music_pachong.items import SongItem


class MiguMusicSpider(scrapy.Spider):
    """咪咕音乐歌曲信息爬虫，抓取指定歌手的歌曲名称与风格。"""

    name = "music"
    allowed_domains = ["www.migu.cn"]

    # 搜索关键词，可通过 -a query=xxx 在命令行覆盖
    query = "周杰伦"

    @property
    def start_urls(self):
        return [
            "http://www.migu.cn/search.html?content={}&type=music&_ch=".format(
                quote(self.query)
            )
        ]

    def parse(self, response):
        """解析搜索首页，获取总页数并分发分页请求。"""
        total_pages = response.xpath(
            "//div[@class='pagination text-right']/ul/li[6]/a/text()"
        ).extract_first()

        if not total_pages:
            self.logger.warning("未能解析到总页数，请检查页面结构是否变更。")
            return

        for page in range(1, int(total_pages) + 1):
            url = "http://www.migu.cn/search.html?content={}&type=music&pn={}".format(
                quote(self.query), page
            )
            yield scrapy.Request(url=url, callback=self.parse_song_list, errback=self.handle_error)

    def parse_song_list(self, response):
        """解析歌曲列表页，提取歌曲名与详情链接。"""
        songs = response.xpath("//div[@class='list']/ul/li")
        for song in songs:
            name = song.xpath(".//a/div[@class='info']/h3/span[2]/text()").extract_first()
            href = song.xpath(".//a/@href").extract_first()
            if name and href:
                yield scrapy.Request(
                    url=href,
                    callback=self.parse_song_detail,
                    errback=self.handle_error,
                    meta={"name": name.strip()},
                )

    def parse_song_detail(self, response):
        """解析歌曲详情页，提取歌词内容。"""
        # 咪咕歌词封装在 <div class="lyrics"> 中，每行为一个 <p>
        # 若页面结构变更，调整此 XPath 即可
        lines = response.xpath("//div[@class='lyrics']/p/text()").getall()
        lyrics = "\n".join(line.strip() for line in lines if line.strip())

        item = SongItem()
        item["name"] = response.meta["name"]
        item["lyrics"] = lyrics
        yield item

    def handle_error(self, failure):
        """统一处理请求失败：HTTP 错误、DNS 解析失败、连接超时等。"""
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(
                "[HttpError] url=%s status=%s", response.url, response.status
            )
        elif failure.check(DNSLookupError):
            self.logger.error(
                "[DNSLookupError] url=%s", failure.request.url
            )
        elif failure.check(TCPTimedOutError):
            self.logger.error(
                "[Timeout] url=%s", failure.request.url
            )
        else:
            self.logger.error(
                "[UnknownError] url=%s error=%s", failure.request.url, repr(failure)
            )
