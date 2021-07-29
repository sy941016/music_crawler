#### scrapy
##### 构建项目
###### 创建项目  
scrapy startproject project_name
###### 运行项目  
scrapy crawl name
###### 尝试选择器(在Windows上,使用双引号)
scrapy shell "url"  
response.xpath('//title/text()').extract_first()
###### 存储数据
scrapy crawl project_name -o name.json
##### 配置
###### spiders
1. yield scrapy.Request(url=''. format(),callback=self.funName, meta={})（get请求）
   + url 跳入地址 
   + format url
   + callback 返回函数 
   + meta传入callback函数的值(以字典的形式)
   + self  <=> this
2. yield scrapy.FormRequest(url='',callback= ) (post请求)
3. start_requests(self,response)  
该方法默认使用start_urls的url生成Request
parse(self,response)  
当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法
4. Filtered offsite request to ''    
过滤后的异地请求给了某个网址，导致链接不正常跳转  
使requests不被过滤的方法：
    1. 在aliowed_domains中加入url
    2. scrapy.Request()函数中加入参数dont_filter=Ture
5. 入表唯一标识整合  
from hashlib import md5
item['unique_id'] = md5((event_id + title + publish_date).encode('utf-8')).hexdigest().lower()
6. setting配置
   + DOWNLOAD_DELAY:   
下载器在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度, 减轻服务器压力 支持小数
   + CONCURRENT_REQUESTS:  
Scrapy downloader 并发请求(concurrent requests)的最大值，默认16
   + COOKIES_ENABLED:  
COOKIES_ENABLED为False时,scrapy默认使用settings的cookie  
COOKIES_ENABLED为True时,scrapy把settings的cookie关掉，使用自定义cookie
