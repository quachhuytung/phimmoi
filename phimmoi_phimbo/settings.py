# -*- coding: utf-8 -*-

# Scrapy settings for phimmoi_phimbo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'phimmoi_phimbo'

SPIDER_MODULES = ['phimmoi_phimbo.spiders']
NEWSPIDER_MODULE = 'phimmoi_phimbo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'phimmoi_phimbo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'phimmoi_phimbo.middlewares.PhimmoiPhimboSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'phimmoi_phimbo.middlewares.PhimmoiPhimboDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'phimmoi_phimbo.pipelines.StripKeyPipeline': 100,
   'phimmoi_phimbo.pipelines.FilterDataAttributePipeline': 200,
   'phimmoi_phimbo.pipelines.DirectorProcessorPipeline': 300,
   'phimmoi_phimbo.pipelines.CountryProcessorPipeline': 400,
   'phimmoi_phimbo.pipelines.YearProcessorPipeline': 500,
   'phimmoi_phimbo.pipelines.ResolutionProcessorPipeline': 600,
   'phimmoi_phimbo.pipelines.GenresProcessorPipeline': 700,
   'phimmoi_phimbo.pipelines.ActorsProcessorPipeline': 800,
   'phimmoi_phimbo.pipelines.DescriptionProcessorPipeline': 900,
   'phimmoi_phimbo.pipelines.IdProcessorPipeline': 950,
   'phimmoi_phimbo.pipelines.LinkAdditionPipeline': 960,
   'phimmoi_phimbo.pipelines.TrailerAdditionPipeline': 970,
   'phimmoi_phimbo.pipelines.JsonWriterPipeline': 1000,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
