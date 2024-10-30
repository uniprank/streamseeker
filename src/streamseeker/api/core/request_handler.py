import re
import time
import random

from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from streamseeker.api.core.logger import Logger
logger = Logger().setup(__name__)

class RequestHandler:
    def __init__(self):
        self._user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
        ]

    def get_header(self, url):
        parsed_url = urlparse(url)
        referer = f"{parsed_url.scheme}://{parsed_url.netloc}"

        headers = {
            "User-Agent": random.choice(self._user_agents),
            "Referer": referer
        }
        return headers
    
    def get(self, url, headers=None) -> urlopen:
        if headers is None:
            headers = self.get_header(url)

        request = Request(url, headers=headers)
        try:
            response = urlopen(request, timeout=100)
            return response
        except URLError as e:
            logger.error(f"Error while trying to get the url: {url}")
            logger.error(f"Error: {e}")
            return None
        
    def get_soup(self, url, headers=None):
        response = self.get(url, headers)
        if response is None:
            return None
        
        return self.soup(response)
    
    def soup(self, html):
        if html is None:
            return None
        
        return BeautifulSoup(html, features="html.parser")