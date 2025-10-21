# Scrapy settings for price_scrapingsite project

#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "price_scrapingsite"

SPIDER_MODULES = ["price_scrapingsite.spiders"]
NEWSPIDER_MODULE = "price_scrapingsite.spiders"

#playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"  # Options: "chromium", "firefox", "webkit"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,  # Set to False to debug in a visible browser
    "slow_mo": 100,
    "devtools": True,
    "args": [
        "--disable-blink-features=AutomationControlled",  # Avoid detection
        "--no-sandbox",
        "--disable-setuid-sandbox",
    ], 
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "price_scrapingsite (+https://www.barnesandnoble.com/b/series/delicious-in-dungeon-series/_/N-301e)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "price_scrapingsite.middlewares.PriceScrapingsiteSpiderMiddleware": 543,
    
}
LOG_LEVEL = 'DEBUG'
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
     #"price_scrapingsite.middlewares.PriceScrapingsiteDownloaderMiddleware": 543,
    
    'price_scrapingsite.middlewares.RetryUserAgentMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    #'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': None,

    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    #'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
     
     
     
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
    #'scrapy_fake_useragent.providers.FakerProvider',  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
]
FAKEUSERAGENT_FALLBACK = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"



USER_AGENT= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# ROTATING_PROXY_LIST = [
    
#     'proxy1.com:8000',
#     'proxy2.com:8031',
#    #dead one,  'proxy3.com:8032',
# ]

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "price_scrapingsite.pipelines.PriceScrapingsitePipeline": 300,
    'price_scrapingsite.pipelines.SavingToMySQLPipeline': 300,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000  # 60 seconds



#---retry section
RETRY_ENABLED= True
RETRY_TIMES = 10
DOWNLOAD_DELAY= 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]
#[403, 500, 502, 503, 504]
