from data import *
from class_spider import spider
import aiohttp
import asyncio
from aiohttp import ClientSession
from urllib.parse import urljoin, urldefrag, urlsplit, urlparse
from bs4 import BeautifulSoup

spider([('http://www.theluxetravel.com','travel'),('http://www.adaptworldwide.com','marketing')])


#Density('test s dsds', 'testing 123 i am a test')