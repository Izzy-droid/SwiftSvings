# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet.error import (
    TimeoutError, TCPTimedOutError, ConnectionRefusedError,
    ConnectionDone, ConnectError, ConnectionLost
)
from scrapy import signals
from scrapy.core.downloader.handlers.http11 import TunnelError
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class PriceScrapingsiteSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    async def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        async for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start_requests):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        #spider.logger.info("process_start() called in PriceScrapingsiteSpiderMiddleware")
        
        if not hasattr(start_requests, "__aiter__"):
                # Convert generator to async generator
            async def async_generator():
                for request in start_requests:
                    yield request
            start_requests = async_generator()
            
        async for request in start_requests:
            yield request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class PriceScrapingsiteDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        
        
class RetryUserAgentMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)
        self.EXCEPTIONS_TO_RETRY = (
            TimeoutError, TCPTimedOutError, ConnectionRefusedError,
            ConnectionDone, ConnectError, ConnectionLost, TunnelError
        )
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)