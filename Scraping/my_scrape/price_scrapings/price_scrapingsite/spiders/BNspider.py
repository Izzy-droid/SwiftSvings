import scrapy
from scrapy_playwright.page import PageMethod
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from fake_useragent import UserAgent
import logging
import requests
from scrapy import Request
#manga/fig compare price site? 
#target: r/mangaswap, facebook marketplace
#add kinokuniya for later maybe : https://usa.kinokuniya.com/new-releases-manga-en


load_dotenv()

ua = UserAgent(platforms='desktop')
fake_user_agent = ua.random



class BNspiderSpider(scrapy.Spider):
    name = "BNspider"
    allowed_domains=['barnesandnoble.com','api.scraperapi.com']
    start_urls= ['https://www.barnesandnoble.com/s/manga']
    custom_settings = {
      'AUTOTHROTTLE_DEBUG': True,
      'AUTOTHROTTLE_START_DELAY' : 5,
      'AUTOTHROTTLE_MAX_DELAY': 60,
      'AUTOTHROTTLE_TARGET_CONCURRENCY':2.0, 
      'DOWNLOAD_DELAY': 3, 
      "CONCURRENT_REQUESTS": 4,
      "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 3,
      'PLAYWRIGHT_LAUNCH_OPTIONS' : {
    
 }
}
    
    
    def start_requests(self):
        base_url = 'https://www.barnesandnoble.com/s/manga'
        
       
       
        yield scrapy.Request(
            base_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                         'Accept-Language': 'en-US,en;q=0.9',
                         }, 
                meta={
            'playwright': True,
            'playwright_include_page': True,
            'playwright_context_kwargs': {  
                'viewport': {'width': 1920, 'height': 1080},
                'ignore_https_errors': True,
                'java_script_enabled': True,
                
            },
            #"autothrottle_dont_adjust_delay": True,
            'playwright_page_methods' : [
                
                PageMethod('wait_for_selector', "#gridView"), 
                PageMethod('evaluate',"window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_timeout', 5000),  
                PageMethod('on', 'console', lambda msg: print(f"Console log: {msg.text}")),
                PageMethod('on', 'pageerror', lambda exc: print(f"Page error: {exc}")),
                PageMethod('route', '**/*', lambda route, request: route.abort() if request.resource_type in ['image', 'font', 'stylesheet'] else route.continue_()),
               
            
              
            ],
        },
        callback=self.parse,
        errback=self.errback
    )

          

    
    def parse(self, response):
        # Log the User-Agent header
        user_agent = response.request.headers.get('User-Agent').decode()
        self.log(f"User-Agent: {user_agent}")
        start_link = "https://www.barnesandnoble.com/"
        linkz = response.xpath("//*[@id='gridView']/div/div/div[1]/div[1]/div/a/@href").getall()
        self.logger.info(f"Found {len(linkz)} product links on {response.url}")

        links = [start_link + link if link.startswith("/") else link for link in linkz]
        for link in links:
            yield response.follow(
            link,
            callback=self.product_parse,
            errback=self.errback,
            meta={'playwright': True}
        )
        
        
        
        next_page = response.xpath("//a[contains(text(),'Next Page') or contains(@class,'next-button')]/@href").get()
        
           
        if next_page:
            self.logger.debug(f"Current page: {next_page}")
            if next_page == "https://www.barnesandnoble.com/s/manga?Nrpp=20&page=51":
                return
            yield response.follow(
            next_page,
            callback=self.parse,
            errback=self.errback,
                meta={'playwright': True} 
            )
        else:
            return     
        
   
       
        
       
            
            
    def product_parse(self,response):
      
        title = response.xpath("//*[@id='pdp-header-info']/h1/text()").get()
        author= response.xpath("//*[@id='key-contributors']/a[1]/text()").get()
        price = response.xpath("//*[@id='pdp-cur-price']/text()").get()
        if price:
            price = price.replace('\xa0', ' ').strip()
       
        
        
        book_type = response.xpath("//*[@id='pdp-info-format']/text()").get()
        desc_parts = response.xpath("//*[contains(@class, 'overview-cntnt')]//text()").getall()
        descript = " ".join([part.strip() for part in desc_parts if part.strip()])
        
        book_img = response.xpath("//*[@id='pdpMainImage']/@src").get()
        # #0
        book_URL =response.xpath("//link[@rel='canonical']/@href").get()
        yield {
            'title': title,
            'author': author,
            'descript': descript,
            'price': price,
            'book_img': book_img,
            'book_type': book_type,
            'book_URL': book_URL
                
        }
        self.logger.debug(f"my titles: {title}")
        self.logger.debug(f"brand: {author}")
        self.logger.debug(f"desc: {descript}")
        self.logger.debug(f"price: {price}")
        self.logger.debug(f"img: {book_img}")
        self.logger.debug(f"img: {book_type}")
        self.logger.debug(f"link: {book_URL}")
        
    
    async def errback(self,failure):
        page= failure.request.meta.get("playwright_page")
        if page:
             self.log("Closing Playwright page due to failure.")
             await page.close()
        self.log(f"Request failed: {failure}")
             #self.crawler.engine.slot.scheduler.close_page(page)
             
  