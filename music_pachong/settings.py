# -*- coding: utf-8 -*-

# Scrapy settings for music_pachong project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'music_pachong'

SPIDER_MODULES = ['music_pachong.spiders']
NEWSPIDER_MODULE = 'music_pachong.spiders'


# 模拟浏览器 User-Agent
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# 咪咕不允许爬虫访问，需要关闭该选项
ROBOTSTXT_OBEY = False

# 最大并发请求数
CONCURRENT_REQUESTS = 8

# 请求间隔（秒），减轻服务器压力
DOWNLOAD_DELAY = 1

# 禁用 Cookie，减少轨迹
COOKIES_ENABLED = False

# 禁用 Telnet 控制台
TELNETCONSOLE_ENABLED = False

# 启用 Pipeline
ITEM_PIPELINES = {
    "music_pachong.pipelines.JsonPipeline": 300,
}

# 启用自动限速，动态调整请求频率
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# 请求超时（秒）
DOWNLOAD_TIMEOUT = 15

# 异常重试配置
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
}
RETRY_ENABLED = True
RETRY_TIMES = 3                          # 最多重试 3 次
RETRY_HTTP_CODES = [500, 502, 503, 504, 429, 408]  # 触发重试的 HTTP 状态码

# 启用 HTTP 缓存（调试时有用，生产环境可关闭）
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 3600
#HTTPCACHE_DIR = 'httpcache'
