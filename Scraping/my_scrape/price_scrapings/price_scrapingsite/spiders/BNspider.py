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
#target: barnesand nobles(1st try), r/mangaswap, facebook marketplace, amiami, goodsmile?
#add kinokuniya for later maybe : https://usa.kinokuniya.com/new-releases-manga-en

#TODO: add img, and fix up mySQL bleh
load_dotenv()

# def get_scraperapi_url(url):
#     API_KEY =os.getenv('API_KEY')
#     payload = {'api_key': API_KEY, 'url': url, 'follow_redirect': 'false', 'output_format': 'json', 'autoparse': 'true', 'country_code': 'us', 'device_type': 'desktop', 'render': 'true', 'premium': 'true'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url

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
      
}
    
    
    async def start(self):
        base_url = 'https://www.barnesandnoble.com/s/manga'
        
        #scraper_url = get_scraperapi_url(base_url)
       
        yield scrapy.Request(
            base_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                         'Accept-Language': 'en-US,en;q=0.9',
                         }, 
                meta={
            'playwright': True,
            'playwright_include_page': True,
            #"autothrottle_dont_adjust_delay": True,
            'playwright_page_methods' : [
                
                PageMethod('wait_for_load_state', 'networkidle'),
                PageMethod('evaluate',"window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_timeout', 5000),  
                PageMethod('on', 'console', lambda msg: print(f"Console log: {msg.text}")),
                PageMethod('on', 'pageerror', lambda exc: print(f"Page error: {exc}")),
                PageMethod('route', '**/*', lambda route, request: route.abort() if request.resource_type in ['image', 'font', 'stylesheet'] else route.continue_()),
                PageMethod('route', '**/*', lambda route, request: print(request.resource_type) or route.continue_()),
            
              
            ],
        },
        callback=self.parse,
        errback=self.errback
    )

          

    
    def parse(self, response):
        # Log the User-Agent header
        user_agent = response.request.headers.get('User-Agent').decode()
        self.log(f"User-Agent: {user_agent}")



# 1 element should have a title, author,prices, book_types, book_URLs, book_imgs

# const results = Array.from(document.querySelectorAll('#gridView > div > div')).map(container => {
#     // Return an object containing the container's ID
#     // and a true array of its child HTML elements.
#     return {
#         id: container.id,
#         children: Array.from(container.children)
#     };
# });









        
        #this is for the books and what will be scraped
        # /html/body/main/div[2]/div[1]/div[2]/div[2]/div/div/section[2]/div/div[1]/div[1]/div[1]/div/a/img
        # //*[@id="gridView"]/div/div[1]/div[1]/div[1]/div/a/img
        titles = response.xpath("//*[@id='gridView']/div/div/div[2]/div[1]/a[@title]/@title").getall()
        authors = response.xpath("//*[@id='gridView']/div/div/div[2]/div[2]/a[1]/text()").getall()
        prices = response.xpath("//*[@id='gridView']/div/div/div[2]/div[4]/div/a/span[2]/text()").getall()
        book_types= response.xpath("//*[@id='gridView']/div/div/div[2]/div[4]/div/a/span[1]/text()").getall()
        book_URLs= response.xpath("//*[@id='gridView']/div/div/div[2]/div[1]/a/@href").getall()
        
        #starting url for clarity
        start_URL= "https://www.barnesandnoble.com"
        #cleaning \n from the needed attributes
        cleaned_prices= [price.strip() for price in prices]
        cleaned_bookTypes=[book_type.strip() for book_type in book_types]

   
        cleaned_bookURLs= [start_URL + url if url.startswith("/") else url for url in book_URLs]
        
        book_imgs = response.xpath("//div[1]/div/a/img/@src").getall()
        #parsing..
        for title, author, price, book_img, book_type, book_URL in zip(titles, authors, cleaned_prices, book_imgs, cleaned_bookTypes, cleaned_bookURLs):
                    yield {'title': title,
                        'author': author,
                        'price': price,
                        'book_img': book_img,
                        'book_type': book_type,
                        'book_URL': book_URL
                   }
        
        #debugging portion for scraped items
        self.logger.debug(f"Extracted titles: {titles}")
        self.logger.debug(f"Extracted authors: {authors}")
        self.logger.debug(f"Extracted prices: {cleaned_prices}")
        self.logger.debug(f"Extracted formats: {cleaned_bookTypes}")
        self.logger.debug(f"Extracted formats: {cleaned_bookURLs}")
       
 
     
       
        
       
     
        # next_page = response.xpath("//a[@class='next-button']/@href").get()
        # self.logger.debug(f"Current page: {response.url}")
       

        #for i in 
        if next_page =="https://www.barnesandnoble.com/s/manga?Nrpp=20&page=51": 
                return
        else:
            yield response.follow(
                url =next_page,
                callback=self.product_parse,
                errback=self.errback,
                meta={'playwright': True} 
            )
    def product_parse(self,response):
        pass
      
    async def errback(self,failure):
        page= failure.request.meta.get("playwright_page")
        if page:
             self.log("Closing Playwright page due to failure.")
             await page.close()
        self.log(f"Request failed: {failure}")
             #self.crawler.engine.slot.scheduler.close_page(page)
             
  