import scrapy
from scrapy_playwright.page import PageMethod
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import logging
import requests
#made for goodsmile
#use show more results instead of next page
load_dotenv()

# def get_scraperapi_url(url):
#     API_KEY =os.getenv('API_KEY')
#     payload = {'api_key': API_KEY, 'url': url, 'follow_redirect': 'false', 'output_format': 'json', 'autoparse': 'true', 'country_code': 'us', 'device_type': 'desktop', 'render': 'true', 'premium': 'true'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url




class GSspiderSpider(scrapy.Spider):
    name = "GSspider"
    allowed_domains=['goodsmileus.com','api.scraperapi.com']
    start_urls= ['https://www.goodsmileus.com/tags/available-now-4?products%5Bpage%5D=14&products%5BrefinementList%5D%5Bcategory_name%5D%5B0%5D=Figures']

    
    
    def start_requests(self):
        base_url = 'https://www.goodsmileus.com/tags/available-now-4?products%5Bpage%5D=14&products%5BrefinementList%5D%5Bcategory_name%5D%5B0%5D=Figures'
        
       
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
                #to handle show results button
                PageMethod('evaluate', "document.querySelector('.ais-InfiniteHits-loadMore').classList.contains('disabled')"),
                PageMethod('click', '.ais-InfiniteHits-loadMore'),
                
                PageMethod(
                 'evaluate',
                """
                async () => {
                    const loadMoreButton = document.querySelector('.ais-InfiniteHits-loadMore');
                    for (i = 0; i< 10; i++) {
                        loadMoreButton.click();
                        await new Promise(resolve => setTimeout(resolve, 2000)); // time for loading
                }
            }
                """
                ),
                    
                    
                PageMethod("wait_for_load_state", "domcontentloaded"),
                PageMethod('evaluate',"window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_timeout', 120000),  
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
        
        titles = response.xpath("//*[@id='hits2']/div/ol/li/h3/a/text()").getall()
        
        figure_imgs= response.xpath("//*[@id='hits2']/div/ol/li/div[1]/a/img/@src").getall()
        
        #COME BACK TO THIS FOR NEEDED PAGINATION
        #brand = response.xpath("//*[@id='gridView']/div/div/div[2]/div[2]/a[1]/text()").getall()
        
        # if  is not None:
            
        
        prices = response.xpath("//*[@id='hits2']/div/ol/li/p/text()").getall()
        
        #come back to figure tags later
        #have an if response.xpath is there then extract it, otherwise disregard it
        #figure_tags= ' '
        
        
        
        inStock_figure_tags = response.xpath("//*[@id='hits2']/div/ol/li/div[2]/a[1]/span/text()").getall()
        
        #check if the tags are there, if so add it to the tagss if not, leave it blank
        #preserve it's placement.
        
        
        # limitedStock_figure_tags = []
        
        # limited = response.xpath("//*[@id='hits2']/div/ol/li/div[2]/a[2]/span[@class='tag-red']/text()").getall()
        
        # for i in range(len(titles)):
            
        #     if len(limitedStock_figure_tags) < len(titles):
        #         limitedStock_figure_tags += [limited[i]] * (len(titles) - len(limited))
        #             # limitedStock_figure_tags.append(limited[item])
        #     else:
        #         limitedStock_figure_tags.append('None')
        
        # enumerate(limitedStock_figure_tags= response.xpath("//*[@id='hits2']/div/ol/li/div[2]/a[2]/span[@class='tag-red']/text()").getall())
       
        # if len(limitedStock_figure_tags) < len(titles) :
        #     limitedStock_figure_tags += ['None'] * (len(titles) - len(limitedStock_figure_tags))
        
           

            
            
            
        figure_URLs= response.xpath("//*[@id='hits2']/div/ol/li/h3/a/@href").getall()
        
        #starting url for clarity
        start_URL= "https://www.goodsmileus.com"

   
        cleaned_figureURLs= [start_URL + url if url.startswith("/") else url for url in figure_URLs]
        
        #parsing..
        for title, price, inStock_figure_tag, figure_img, cleanedfigure_URL in zip(titles, prices, inStock_figure_tags, figure_imgs, cleaned_figureURLs):
                    yield {'title': title,
                        'price': price,
                        'inStock_figure_tags':  inStock_figure_tag,
                        #'limitedStock_figure_tags':limitedStock_figure_tag,
                        'figure_img': figure_img,
                        'figure_URL': cleanedfigure_URL
                        
                   }
        
        #debugging portion for scraped items
        self.logger.debug(f"Extracted titles: {titles}")
        self.logger.debug(f"Extracted authors: {prices}")
        # self.logger.debug(f"Extracted prices: {figure_tags}")
        self.logger.debug(f"Extracted formats: {figure_imgs}")
        self.logger.debug(f"Extracted formats: {cleaned_figureURLs}")
        #self.logger.debug(f"Extracted tag: {limitedStock_figure_tags}")
       
    
      
    async def errback(self,failure):
        page= failure.request.meta.get("playwright_page")
        if page:
             self.log("Closing Playwright page due to failure.")
             await page.close()
        self.log(f"Request failed: {failure}")
             #self.crawler.engine.slot.scheduler.close_page(page)
             
  
