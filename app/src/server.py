import os
import re
import scrapy
from flask import Flask
server = Flask(__name__)

class MySpider(scrapy.Spider):
    name = 'MEDIA_SERVER'
    media_server = os.environ.get('MEDIA_SERVER')
    media_regex = os.environ.get('MEDIA_REGEX')
    start_urls = [ media_server ]
    rules = (
        # Extract links ending with a forward slash, and follow links from them
        Rule(LinkExtractor(allow=('/$', ))),
    )
    def parse(self, response):
        for href in response.xpath('//a/@href').getall():
            match = re.search(media_regex, href)
            if match:
                yield href

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)



@server.route("/")
 def hello():
    # limit rate to prevent DOS style attacks
   
    # crawl webpage and filter all desired file types
     
    
    # sync with output directory
    return "Hello World!"

if __name__ == "__main__":
   server.run(host='0.0.0.0') 
