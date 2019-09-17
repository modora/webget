import unittest
from pathlib import Path

from webget.pipelines.save_page_source import SavePagePipeline


class TestURLParser(unittest.TestCase):
    def testRoot(self):
        # https://example.com/
        # 	domain = example.com
        # 	url_path = index.html
        # 	save_path = ${DOWNLOAD_DIR}/example.com/index.html
        url = "https://example.com/"
        (domain, url_path) = SavePagePipeline._parse_url(url)

        self.assertEqual(domain, "example.com")
        self.assertEqual(url_path, "index.html")

    def testNested(self):
        # https://example.com/foo/bar.php
        # 	domain = example.com
        # 	url_path = foo/bar.php.html
        # 	save_path = ${DOWNLOAD_DIR}/example.com/foo/bar.php.html
        url = "https://example.com/foo/bar.php"
        (domain, url_path) = SavePagePipeline._parse_url(url)

        self.assertEqual(domain, "example.com")
        self.assertEqual(url_path, "foo/bar.php.html")

    def testSubdomain(self):
        # https://subdomain.example.com/
        # 	domain = subdomain.example.com
        # 	url_path = index.html
        # 	save_path = ${DOWNLOAD_DIR}/subdomain.example.com/index.html
        url = "https://subdomain.example.com/"
        (domain, url_path) = SavePagePipeline._parse_url(url)

        self.assertEqual(domain, "subdomain.example.com")
        self.assertEqual(url_path, "index.html")

    def testHTMLSuffix(self):
        # https://example.com/hello.html
        # 	domain = example.com
        # 	url_path = hello.html
        # 	save_path = ${DOWNLOAD_DIR}/example.com/hello.html
        url = "https://example.com/hello.html"
        (domain, url_path) = SavePagePipeline._parse_url(url)

        self.assertEqual(domain, "example.com")
        self.assertEqual(url_path, "hello.html")


class TestSavePath(unittest.TestCase):
    def testRoot(self):
        # https://example.com/
        # 	domain = example.com/
        # 	url_path = index.html
        # 	save_path = ${DOWNLOAD_DIR}/example.com/index.html
        domain = "example.com/"
        url_path = "index.html"
        save_path = SavePagePipeline._format_save_path(
            domain, url_path, save_dir="/download_dir"
        )
        self.assertEqual(save_path, Path("/download_dir/example.com/index.html"))

    def testRootImplied(self):
        # https://example.com
        # 	domain = example.com
        # 	url_path = index.html
        # 	save_path = ${DOWNLOAD_DIR}/example.com/index.html
        domain = "example.com"
        url_path = "index.html"
        save_path = SavePagePipeline._format_save_path(
            domain, url_path, save_dir="/download_dir"
        )
        self.assertEqual(save_path, Path("/download_dir/example.com/index.html"))

    def testNested(self):
        # https://example.com/foo/bar.php
        # 	domain = example.com
        # 	url_path = foo/bar.php.html
        # 	save_path = ${DOWNLOAD_DIR}/example.com/foo/bar.php.html
        domain = "example.com"
        url_path = "foo/bar.php.html"
        save_path = SavePagePipeline._format_save_path(
            domain, url_path, save_dir="/download_dir"
        )
        self.assertEqual(save_path, Path("/download_dir/example.com/foo/bar.php.html"))

    def testSubdomain(self):
        # https://subdomain.example.com/
        # 	domain = subdomain.example.com
        # 	url_path = index.html
        # 	save_path = ${DOWNLOAD_DIR}/subdomain.example.com/index.html
        domain = "subdomain.example.com"
        url_path = "index.html"
        save_path = SavePagePipeline._format_save_path(
            domain, url_path, save_dir="/download_dir"
        )
        self.assertEqual(
            save_path, Path("/download_dir/subdomain.example.com/index.html")
        )
