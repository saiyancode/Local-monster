from data import *
import aiohttp
import asyncio
from aiohttp import ClientSession
from urllib.parse import urljoin, urldefrag, urlsplit, urlparse
from bs4 import BeautifulSoup

AgentList = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
             "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
             "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0"]

class spider():

    data = []
    queue = []

    @classmethod
    async def get_body(self,url):
        async with ClientSession() as session:
            async with session.get(url, timeout=60) as response:
                response = await response.read()
                # print(response)
                return response

    @classmethod
    async def handle_task(self,task_id, work_queue, Project,queue):
        while not work_queue.empty():
            queue_url = await work_queue.get()
            # Unpack the original tuple list passed to the spider
            keyword = [x[1] for x in queue if x[0] == queue_url]
            print(keyword[0])
            print('Now crawling ' + queue_url + " | there are " + str(len(self.queue)) + " links in queue")
            try:
                body = await self.get_body(queue_url)
                #meta = meta_data()
                density = Density(keyword,body)
            except Exception as e:
                print(e)
                pass

    @classmethod
    def results(self):
        return self.data

    def __init__ (self, queue):
        q = asyncio.Queue()
        [self.queue.append(i[0]) for i in queue]
        [q.put_nowait(url) for url in self.queue]
        loop = asyncio.get_event_loop()
        tasks = [self.handle_task(task_id, q, 'list', queue) for task_id in range(3)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

