import scrapy
from scrapy_playwright.page import PageMethod
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import logging
#COME BACK TO THIS FOR THE LOGIC OF THE PAGINATION
#unfinished
class BNs_mainspiderSpider(scrapy.Spider):
    name = "mainspider"
    allowed_domains = ["www.barnesandnoble.com"]
    start_urls = ["https://www.barnesandnoble.com/b/books/graphic-novels-comics-manga/_/N-29Z8q8Z2y35"]

    
    
    
    def start_requests(self):
        base_url = 'https://www.barnesandnoble.com/b/books/graphic-novels-comics-manga/_/N-29Z8q8Z2y35'
        
   
       
        yield scrapy.Request(
            base_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                         'Accept-Language': 'en-US,en;q=0.9',
                         }, 
                meta={
            'playwright': True,
            'playwright_include_page': True,
            'playwright_page_methods' : [
                PageMethod('wait_for_selector', '#manga-publisher-wrapper', timeout=120000),
                PageMethod('evaluate', "document.querySelector('#manga-publisher-wrapper') !== null"),
                PageMethod('wait_for_load_state', 'networkidle'),
                PageMethod('evaluate',"window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_timeout', 5000),  
                PageMethod('on', 'console', lambda msg: print(f"Console log: {msg.text}")),
                PageMethod('on', 'pageerror', lambda exc: print(f"Page error: {exc}")),
                PageMethod('route', '**/*', lambda route, request: route.abort() if request.resource_type in ['image', 'font', 'stylesheet'] else route.continue_()),
                #PageMethod('evaluate', "document.querySelector('#gridView') !== null"),
                #PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                #PageMethod('wait_for_timeout', 3000),  # Wait for 3 seconds after scrolling
                
                #PageMethod('wait_for)scelector',"div. :nth-child(11)"), # 10 per page
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
        authors = response.xpath("//*[@id='gridView']/div/div/div[2]/div[2]/a[1]/text()").getall()
        prices = response.xpath("//*[@id='gridView']/div/div/div[2]/div[4]/div/a/span[2]/text()").getall()
        book_types= response.xpath("//*[@id='gridView']/div/div/div[2]/div[4]/div/a/span[1]/text()").getall()
        book_URLs= response.xpath("//*[@id='gridView']/div/div/div[2]/div[1]/a/@href").getall()
        
        #starting url for bookurl
        start_URL= "https://www.barnesandnoble.com"
        
        cleaned_prices= [price.strip() for price in prices]
        cleaned_bookTypes=[book_type.strip() for book_type in book_types]

   
        cleaned_bookURLs= [start_URL + url if url.startswith("/") else url for url in book_URLs]
        
        #parsing..
        for title, author, book_type, price, book_URL in zip(titles, authors, cleaned_bookTypes, cleaned_prices, cleaned_bookURLs):
                    yield {'title': title,
                        'author': author,
                        'price': price,
                        'book-type': book_type,
                        'book_URL': book_URL
                   }
        
        
        next_page=response.xpath("//*/a[@class='next-button']/@href").get()
        self.logger.debug(f"Pagination link: {next_page}")
        #FIX LOGIC BELOW
        startt= response.xpath("//*[@id='manga-publisher-wrapper']/a/@href").getall()
        if startt:
            self.logger.debug(f"test: {startt}")
            for i in startt: 
                self.logger.debug(i)
                complete_url = start_URL + i if i.startswith("/") else i
                
                yield scrapy.Request( 
                url = complete_url, 
                callback = self.parse,
                errback=self.errback
        ) 
        else:
            self.logger.debug("nada.")
     
    async def errback(self,failure):
        page= failure.request.meta.get("playwright_page")
        if page:
             self.log("Closing Playwright page due to failure.")
             await page.close()
        self.log(f"Request failed: {failure}")
            
             
  


