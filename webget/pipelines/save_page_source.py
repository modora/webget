from urllib.parse import urlparse
from pathlib import Path
from logging import getLogger

from webget import app_data

logger = getLogger('SavePagePipeline')

DOWNLOAD_DIR = Path(app_data, 'downloads')

class SavePagePipeline:
	@staticmethod
	def _parse_url(url: str) -> tuple:
		# https://example.com/
		# 	domain = example.com
		# 	url_path = index.html
		#	save_path = ${DOWNLOAD_DIR}/example.com/index.html
		# https://example.com/foo/bar.php
		# 	domain = example.com
		# 	url_path = foo/bar.php.html
		#	save_path = ${DOWNLOAD_DIR}/example.com/foo/bar.php.html
		# https://subdomain.example.com/
		# 	domain = subdomain.example.com
		#	url_path = index.html
		#	save_path = ${DOWNLOAD_DIR}/subdomain.example.com/index.html
		domain = urlparse(url).netloc
		url_path = (urlparse(url).path[1:] or 'index')
		if not url_path.endswith('.html'):
			url_path += '.html'
		return (domain, url_path)

	@staticmethod
	def _format_save_path(domain, url_path, save_dir=DOWNLOAD_DIR) -> Path:
		save_dir = Path(save_dir)
		return save_dir.joinpath(domain, url_path)

	def process_item(self, item, spider):
		response = item.get('response')
		if not response:
			return item
		
		# Unpack the parsed items from the spider
		url = response.url
		page_source = response.text

		# Save the page source to the target directory
		(domain, url_path) = self._parse_url(url)
		save_path = self._format_save_path(domain, url_path)
		save_path.parent.mkdir(parents=True, exist_ok=True)
		save_path.write_text(page_source)  # this will override existing files

		logger.debug(f'Saved {url} to {save_path}')

		return item