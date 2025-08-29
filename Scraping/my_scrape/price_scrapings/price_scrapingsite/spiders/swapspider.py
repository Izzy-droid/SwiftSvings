#for mangaswap subreddit
import scrapy
from scrapy_playwright.page import PageMethod
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import logging
import requests
load_dotenv()

# def get_scraperapi_url(url):
#     API_KEY =os.getenv('API_KEY')
#     payload = {'api_key': API_KEY, 'url': url, 'follow_redirect': 'false', 'output_format': 'json', 'autoparse': 'true', 'country_code': 'us', 'device_type': 'desktop', 'render': 'true', 'premium': 'true'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url


#have AI filter through the prices and titles? bleh


class SwapspiderSpider(scrapy.Spider):
    name = "Swapspider"
    allowed_domains=['reddit.com','api.scraperapi.com']
    start_urls= ['https://www.reddit.com/r/mangaswap/']

    
    
    def start_requests(self):
        base_url = 'https://www.reddit.com/r/mangaswap/'
        
        #scraper_url = get_scraperapi_url(base_url)
       
        yield scrapy.Request(
            base_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                         'Accept-Language': 'en-US,en;q=0.9',
                         }, 
                meta={
            'playwright': True,
            'playwright_include_page': True,
            'playwright_page_methods' : [
                
                PageMethod('wait_for_load_state', 'networkidle'),
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

        
        #this is for the books and what will be scraped
        titles = response.xpath("//*[@id='gridView']/div/div/div[2]/div[1]/a[@title]/@title").getall()
        users = response.xpath("//*[@id='gridView']/div/div/div[2]/div[2]/a[1]/text()").getall()
        prices = response.xpath("//*[@id='gridView']/div/div/div[2]/div[4]/div/a/span[2]/text()").getall()
        book_imgs= response.xpath("//*[@id='gridView']/div/div/div[2]/div[4]/div/a/span[1]/text()").getall()
        book_URLs= response.xpath("//*[@id='gridView']/div/div/div[2]/div[1]/a/@href").getall()
        
        #starting url for clarity
        start_URL= "https://www.reddit.com"
        #cleaning \n from the needed attributes
        cleaned_prices= [price.strip() for price in prices]
        cleaned_bookTypes=[book_type.strip() for book_type in book_types]

   
        cleaned_bookURLs= [start_URL + url if url.startswith("/") else url for url in book_URLs]
        
        #parsing..
        for title, author, book_type, price, book_URL in zip(titles, authors, cleaned_bookTypes, cleaned_prices, cleaned_bookURLs):
                    yield {
                        'title': title,
                        'author': author,
                        'price': price,
                        'book-type': book_type,
                        'book_URL': book_URL
                   }
        
        #debugging portion for scraped items
        self.logger.debug(f"Extracted titles: {titles}")
        self.logger.debug(f"Extracted authors: {authors}")
        self.logger.debug(f"Extracted prices: {cleaned_prices}")
        self.logger.debug(f"Extracted formats: {cleaned_bookTypes}")
        self.logger.debug(f"Extracted formats: {cleaned_bookURLs}")
       
     
       
        
        #next_page = response.xpath("//*[@id='searchGrid']/div/section[3]/ul/li[7]/a/@href").get()
        next_page=response.xpath("//*/a[@class='next-button']/@href").get()
        self.logger.debug(f"Pagination link: {next_page}")
        if next_page =="https://www.barnesandnoble.com/s/manga?Nrpp=20&page=51": 
            return
            # for i in range(1,51):
            #     next_url = f"https://www.barnesandnoble.com/s/manga?Nrpp=20&page={i}"
        else: # self.logger.debug(f"Pagination link: {next_url}")
            self.logger.debug(f"Pagination link: {next_page}")
            yield scrapy.Request( 
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
             
  