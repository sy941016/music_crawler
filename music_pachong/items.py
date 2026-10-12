import scrapy


class SongItem(scrapy.Item):
    name = scrapy.Field()    # 歌曲名称
    lyrics = scrapy.Field()  # 歌词内容
