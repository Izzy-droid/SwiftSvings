import scrapy
from scrapy_playwright.page import PageMethod
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import logging
import requests

#for amiami

load_dotenv()
#start_url = 'https://www.amiami.com/eng/search/list/?s_st_list_newitem_available=1&s_st_condition_flg=1&s_cate2=1298&pagecnt=1'
#go until page 10

# def get_scraperapi_url(url):
#     API_KEY =os.getenv('API_KEY')
#     payload = {'api_key': API_KEY, 'url': url, 'follow_redirect': 'false', 'output_format': 'json', 'autoparse': 'true', 'country_code': 'us', 'device_type': 'desktop', 'render': 'true', 'premium': 'true'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url


#COME BACK TO LATER!!!!!


class amispiderSpider(scrapy.Spider):
    name = "amispider"
    allowed_domains=['amiami.com','api.scraperapi.com']
    start_urls= ['https://www.amiami.com/eng/search/list/?s_st_list_newitem_available=1&s_st_condition_flg=1&s_cate2=1298&pagecnt=1']
    
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.amiami.com/eng/search/list/?s_st_list_newitem_available=1&s_st_condition_flg=1&s_cate2=1298&pagecnt=1',
     }
    
    
    def start_requests(self):
        base_url = 'https://www.amiami.com/eng/search/list/?s_st_list_newitem_available=1&s_st_condition_flg=1&s_cate2=1298&pagecnt=1'
        
        #scraper_url = get_scraperapi_url(base_url)
       
        yield scrapy.Request(
            base_url,
            # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            #              'Accept-Language': 'en-US,en;q=0.9',
            #              'Referer': 'https://www.amiami.com/eng/search/list/?s_st_list_newitem_available=1&s_st_condition_flg=1&s_cate2=1298&pagecnt=1',
            #              }, 
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
        
        
        titles = response.xpath("//*[@id='__nuxt']/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/section/div/ul/li/a/div[2]/p[1]/text()").getall()
        figure_brands = response.xpath("//*[@id='__nuxt']/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/section/div/ul/li/a/div[2]/p[2]/text()").getall()
        prices = response.xpath("//*[@id='__nuxt']/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/section/div/ul/li/a/div[2]/p[3]/text()").getall()
        #figure_types= response.xpath("").getall()
        figure_URLs= response.xpath("//*[@id='__nuxt']/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/section/div/ul/li/a/@href").getall()
        
        #starting url for clarity
        start_URL= "https://www.amiami.com"
        
        
      
        
        #strip , from prices
        prices = [price.replace(",", "").strip() for price in prices]
        #turn each price into a float then back to a list?
        #convert values
        convert = [float(price) * .006783 for price in prices]
        #f string to add sign and approx,
        conversion_prices = [f"${price:.2f} (approx.)" for price in convert]
        

   
        cleanedfigure_URLs= [start_URL + url if url.startswith("/") else url for url in figure_URLs]
        
        figure_imgs= response.xpath("//*[@id='__nuxt']/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/section/div/ul/li/a/div[1]/p/img/@src").getall()
        #parsing..
        for title, figure_brand, conversion_price, figure_img, cleanedfigure_URL in zip(titles, figure_brands,  conversion_prices, figure_imgs, cleanedfigure_URLs):
                    yield {'title': title,
                        'price': conversion_price,
                        'brand': figure_brand,
                        'figure_img': figure_img,
                        'figure_URL': cleanedfigure_URL
                   }
        
        #debugging portion for scraped items
        self.logger.debug(f"Extracted titles: {titles}")
        self.logger.debug(f"Extracted prices: {conversion_prices}")
        self.logger.debug(f"Extracted formats: {figure_brands}")
        self.logger.debug(f"Extracted formats: {cleanedfigure_URLs}")
       
     
     
       
        
        
        
        #https://www.amiami.com/eng/search/list/?s_st_list_newitem_available=1&s_st_condition_flg=1&s_cate2=1298&pagecnt=1
        #                                                                                                                ^ change this for pagination, fuck the previous strat
        
          
        next_page = "https://www.amiami.com/eng/search/list/?s_st_list_newitem_available=1&s_st_condition_flg=1&s_cate2=1298&pagecnt="
        for i in range(2,11):
            pagination_pages =(f"{next_page}{i}")
            self.logger.debug(f"Pagination link: {pagination_pages}")
            yield scrapy.Request( 
                url = pagination_pages, 
                headers= self.headers,
                meta={
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                PageMethod('wait_for_load_state', 'networkidle'),
                PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_timeout', 5000),
                ],
                },
                callback = self.parse,
                errback=self.errback
        ) 
    
      
    async def errback(self,failure):
        page= failure.request.meta.get("playwright_page")
        if page:
             self.log("Closing Playwright page due to failure.")
             await page.close()
        self.log(f"Request failed: {failure}")
            
             
  
