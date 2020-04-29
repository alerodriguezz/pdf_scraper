import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class PdfUrlSpider(CrawlSpider):
    
    #NAME is required. It is how we refer to the PdfUrlClass in the cmd
    name = 'pdf_url'

    #Every link that is scanned must be from this list 
    allowed_domains = ['adobe.com']

    #this is the url we will start from (Check all links of this webpage(s) first and then go deeper)
    start_urls = ['https://www.adobe.com']
    
    #each rules parameter specifies which rule we have to folow for the link
    #1. allows all links to be extracted 
    #2. call parse_httpresponse on each extracted link 
    #3. follow all links ("click" on them so we can check all the links on THAT webpage too)
    rules =[Rule(LinkExtractor(allow=''), callback='parse_httpresponse', follow=True)]

    def parse_httpresponse(self, response):
        return