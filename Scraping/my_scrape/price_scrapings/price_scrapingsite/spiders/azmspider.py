#for amazon manga...

#url= 'https://www.amazon.com/s?k=manga+book&crid=1ZXFJ567FXDXC&sprefix=manga+boo%2Caps%2C212&ref=nb_sb_noss_2'
import scrapy
from scrapy_playwright.page import PageMethod
import os
from dotenv import load_dotenv
from urllib.parse import urlencode, urljoin
from fake_useragent import UserAgent

import logging
import requests
load_dotenv()

# def get_scraperapi_url(url):
#     API_KEY =os.getenv('API_KEY')     
#     payload = {'api_key': API_KEY, 'url': url, 'follow_redirect': 'false', 'country_code': 'us', 'device_type': 'desktop', 'render': 'true', 'premium': 'true'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url


ua = UserAgent(platforms='desktop')
fake_user_agent = ua.random

class AzmspiderSpider(scrapy.Spider):
    name = "azmspider"
    allowed_domains=['amazon.com','api.scraperapi.com']
    start_urls= ['https://www.amazon.com/manga/s?k=manga&i=stripbooks&rh=n%3A283155%2Cn%3A4367&dc&qid=1752971757&rnid=2941120011&xpid=4WxldIwOnAH9d&ref=sr_pg_1']
    custom_settings = {
        "USER_AGENT": fake_user_agent,
        'AUTOTHROTTLE_DEBUG': True,
        'AUTOTHROTTLE_START_DELAY' : 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY':2.0,
    }
    
    
    def start_requests(self):
        base_url = 'https://www.amazon.com/manga/s?k=manga&i=stripbooks&rh=n%3A283155%2Cn%3A4367&dc&qid=1752971757&rnid=2941120011&xpid=4WxldIwOnAH9d&ref=sr_pg_1'
        
        #scraper_url = get_scraperapi_url(base_url)
       
        yield scrapy.Request(
            base_url,
            headers={'User-Agent': self.settings['USER_AGENT'],
                     'Accept-Language': 'en-US,en;q=0.9',
                        }, 
                meta={
            'playwright': True,
            'playwright_include_page': True,
            
            
            "handle_httpstatus_list": [301, 302, 307],
            'playwright_page_methods' : [
                PageMethod('wait_for_load_state', 'networkidle'),
                PageMethod('evaluate',"window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_timeout', 12000),  
                PageMethod('screenshot', path='screenshot.png'),  
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

        
        #this is for the books and what will be scraped
        
        #look for an id/class in common in this bitch
        #$x("//*[@id="df09c389-6114-401c-87ba-75d15c21f573"]/div/div/div/div/span/div/div/div[3]/div[1]/a/h2/span")
        with open('response.html', 'w',  encoding="utf-8") as f:
            f.write(response.text)
        
        
        #hmm
        with open('response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        #titles = response.xpath("//*/div[1]/a/h2/span/text()").getall()
        #$x("//*/div[@class='sg-col-inner']")
        #$x("//*/div[1][@data-cy='title-recipe']/a/h2/span/text()")
        titles = response.xpath("//div[1][@class='a-section a-spacing-none a-spacing-top-small s-title-instructions-style']/a/h2/span/text()").getall()
        #IM SO ERECT
        self.logger.debug(f" krill yuorself: {len(titles)}")
    
        #requires pagination below
        #authors = response.xpath("//*/div[3]/div[2]/div[1]/a/span[1]/span[1]/text()").getall()
        
        #TODO: fix prices, book types and book urls xpath then find a way to put in authors
        
        prices = response.xpath("//div[3][@class='a-section a-spacing-none a-spacing-top-small s-price-instructions-style']/div[2]/div[1]/a/span[1]/span[1]/text()").getall()
        
        #FIX THIS ONE
        book_types= response.xpath("//div[3][@class='a-section a-spacing-none a-spacing-top-small s-price-instructions-style']/div[1]/a/text()").getall()
        
        #WIP...
        book_URLs= response.xpath("//div[1][@data-cy='title-recipe']/a/@href").getall()
        
        #starting url for clarity
        start_URL= "https://www.amazon.com"
        
        #cleaning \n from the needed attributes
        cleaned_prices= [price.strip() for price in prices]
        
        self.logger.debug((f" krill yuorself: {len(cleaned_prices)}"))
        
        cleaned_bookTypes=[book_type.strip() for book_type in book_types]
        
        self.logger.debug((f" krill yuorself: {len(cleaned_bookTypes)}"))

        tests= response.xpath("//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[1]/div/span[1]/div/div/div/span").get()
        self.logger.debug(f"Extracted test: {tests}")
   
        cleaned_bookURLs= [start_URL + url if url.startswith("/") else url for url in book_URLs]
        self.logger.debug((f" krill yuorself: {len(cleaned_bookURLs)}"))
        #parsing..
        for title, book_type, price, book_URL in zip(titles, cleaned_bookTypes, cleaned_prices, cleaned_bookURLs):
                    yield {'title': title,
                        #'author': author,
                        'price': price,
                        'book-type': book_type,
                        'book_URL': book_URL
                   }
        
        #debugging portion for scraped items
        self.logger.debug(f"Extracted titles: {titles}")
        #self.logger.debug(f"Extracted authors: {authors}")
        self.logger.debug(f"Extracted prices: {cleaned_prices}")
        self.logger.debug(f"Extracted formats: {cleaned_bookTypes}")
        self.logger.debug(f"Extracted formats: {cleaned_bookURLs}")
       
       #PAGINATION POG
     
       
        
        next_page = response.xpath("//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[38]/div/div/span/ul/li[6]/span/a/@href").get()
        
        
        # next_page=response.xpath("//*/a[@class='next-button']/@href").get()
        self.logger.debug(f"Pagination link: {next_page}")
        if next_page =="https://www.amazon.com/s?k=manga&i=stripbooks&rh=n%3A283155%2Cn%3A4367&dc&page=11&qid=1753070819&rnid=2941120011&xpid=4WxldIwOnAH9d&ref=sr_pg_11": 
             return
        
            
         #next_url = f"https://www.barnesandnoble.com/s/manga?Nrpp=20&page={i}"
        else: 
            self.logger.debug(f"Pagination link: {next_page}")
            yield response.follow( 
                url = next_page, 
                callback = self.parse,
                errback=self.errback
            ) 
    
      
    async def errback(self,failure):
        page= failure.request.meta.get("playwright_page")
        if page:
             self.log("Closing Playwright page due to failure.")
             await page.close()
        self.log(f"Request failed: {failure}")
             #self.crawler.engine.slot.scheduler.close_page(page)
             
  