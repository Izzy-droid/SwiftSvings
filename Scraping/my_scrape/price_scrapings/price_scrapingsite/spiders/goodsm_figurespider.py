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






class GSspiderSpider(scrapy.Spider):
    name = "GSspider"
    allowed_domains=['goodsmileus.com','api.scraperapi.com']
    start_urls= ['https://www.goodsmileus.com/search?options%5Bprefix%5D=last&page=1&q=figures']

    
    
    def start_requests(self):
        base_url = 'https://www.goodsmileus.com/search?options%5Bprefix%5D=last&page=1&q=figures'
        
       
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
                # PageMethod('evaluate', "document.querySelector('.ais-InfiniteHits-loadMore').contains('disabled')"),
                # PageMethod('click', '.ais-InfiniteHits-loadMore'),
                
                PageMethod(
                 'evaluate',
                """
                async () => {
                   
                    for (i = 0; i< 10; i++) {
                        const loadMoreButton = document.querySelector("button.btn.py-md.px-xl.rounded-md.mx-auto.mb-md.relative");
                        if (loadMoreButton) {
                            loadMoreButton.click();
                            console.log(`Clicked {i} times`);
                            await new Promise(resolve => setTimeout(resolve, 2000)); // time for loading
                        } else {
                            console.log("No more times.");
                            break;
                        }
                        
                }
            }
                """
                ),
                    
                    
                
                PageMethod('evaluate',"window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_timeout', 120000),  
                PageMethod('on', 'console', lambda msg: print(f"Console log: {msg.text}")),
                PageMethod('on', 'pageerror', lambda exc: print(f"Page error: {exc}")),
                PageMethod("wait_for_selector", "img[src*='/cdn/shop/files']", timeout=10000),

               PageMethod('route', '**/*', lambda route, request: route.abort() if request.resource_type in ['image', 'font', 'stylesheet', 'media'] else route.continue_()),

            
              
            ],
        },
        callback=self.parse,
        errback=self.errback
    )

          

    
    def parse(self, response):
        # Log the User-Agent header
        user_agent = response.request.headers.get('User-Agent').decode()
        self.log(f"User-Agent: {user_agent}")

      
        start_link = "https://www.goodsmileus.com"
       
   
        linkz = response.xpath("//div/div/s-collection-grid/div[2]/div[2]/ul/li/product-card/div/div[2]/div[1]/p/a/@href").getall()
       
        
        links = [start_link + link if link.startswith("/") else link for link in linkz]
        
       
        for link in links:
            self.logger.debug(f"here da link:{link}")
            yield response.follow(
                link,
                callback=self.parse_product,
                meta={'playwright': True}
            )
                
            
           
    def parse_product(self,response):
        title = response.xpath("//div[1]/h1/text()").get()
        brand = response.xpath(("//strong[contains(text(), 'BRAND')]/following-sibling::text()[1]")).get()
        price = response.xpath("//div[1]/span[2]/span/text()").get()
        desc_parts = response.xpath("//div[@id='descriptionContent']//text()").getall()
        descript = " ".join([part.strip() for part in desc_parts if part.strip()])
        figure_img = response.xpath("//img[contains(@srcset, '/cdn/shop/files')]").attrib["src"]
        series_tag = response.xpath("//div[2]/div[3]/a[1]/text()").get()

        figure_url= response.xpath("//link[@rel='canonical']/@href").get()
     
        
        
       
        yield {
            'title': title,
            'brand': brand,
            'descript': descript,
            'price': price,
            'figure_img': figure_img,
            #'series_tag': series_tag,
            'figure_url': figure_url,
            
            
                
        }
        self.logger.debug(f"Extracted titles: {title}")
        self.logger.debug(f"brand: {brand}")
        self.logger.debug(f"desc: {descript}")
     
       
    
      
    async def errback(self,failure):
        page= failure.request.meta.get("playwright_page")
        if page:
             self.log("Closing Playwright page due to failure.")
             await page.close()
        self.log(f"Request failed: {failure}")
             
             
  
