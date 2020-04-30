import scrapy
import re 
from pdf_url.items import PdfUrlItem
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

        if response.status!= 200:
            return None 

        item = PdfUrlItem()
        #check if the link is a pdf
        if b'Content-Type' in response.headers.keys():
            links_to_pdf = 'application/pdf' in str(response.headers['Content-Type'])
        else: 
            return None
        #yes? scrape it 

        #check is content disposition element exists 
        content_disposition_exists = b'Content-Disposition' in response.headers.keys()

        if links_to_pdf:
            if content_disposition_exists:
                item['url']= response.url
                item['filename']= re.search('filename="(.+)"', str(response.headers['Content-Disposition'])).group(1)
            else:
                #scrape specified data(refernenced in items.py)
                item['url'] = response.url
                item['filename'] = response.url.split('/')[-1]
        #no? ignore it and proceed 
        else:
            return None 

        #write data to csv
        print ("wrote...."+ item['filename']+"...to urls.csv")
        print()
        return item