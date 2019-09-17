import urllib
import logging

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 30  # page timeout in seconds
WEB_DRIVER = "chromium"

logger = logging.getLogger(__name__)


class SeleniumDownloaderMiddleware(object):
	# Processes a request in selenium

	def __init__(self, crawler):
		if WEB_DRIVER == "chromium":
			options = webdriver.ChromeOptions()
			options.add_argument("--headless")
			options.add_argument('--no-sandbox')  # required for running as root
			self.driver = webdriver.Chrome(options=options)
		elif WEB_DRIVER == "firefox":
			options = webdriver.FirefoxOptions()
			options.headless = True
			self.driver = webdriver.Firefox(options=options)
		else:
			raise ValueError("Unknown webdriver")

		crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
		crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		return cls(crawler)

	def spider_opened(self, spider):
		spider.logger.info(f"Spider opened: {spider.name}")

	def spider_closed(self, spider):
		spider.logger.info(f"Spider closed: {spider.name}")
		self.driver.quit()

	def process_response(self, request, response , spider):
		if response.status == 200:
			# Process page using selenium
			# Unfortunately, there is no way to inject the page_source into the
			# browser directly so we will have to rerequest the page
			
			self.driver.get(request.url)
			# Wait until the page has completely loaded
			WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
				lambda driver: driver.execute_script("return document.readyState")
				== "complete"
			)
			return HtmlResponse(
				self.driver.current_url,
				body=self.driver.page_source,
				encoding="utf-8",
				request=request,
			)
		else:
			return response