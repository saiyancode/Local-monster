from bs4 import BeautifulSoup
import requests
import time
import re
from urllib.parse import urljoin, urldefrag, urlsplit, urlparse

stop_words = ['the', 'that', 'to', 'as', 'there', 'has', 'and', 'or', 'is', 'not', 'a', 'of', 'but', 'in', 'by', 'on', 'are', 'it', 'if','an']
elements = ['var','ul','li','px','div','script','inline','tr']

class Density():

    def __init__(self,keyword,body):
        body = body.decode('utf-8')
        body = self.clean_page(body)
        result = self.get_density(keyword[0],body)
        self.content_length = result['content_length']
        self.density = result['density']
        self.keyword_occurence = result['keyword_mentions']


    @classmethod
    def clean_page(self,body):
        master = []
        final = []
        FINAL =[]
        # Strip out the sequency of script tags
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', body)
        # Remove blank spaces and split by percieved word
        new = [line for line in cleantext.split('\n') if line.strip() != '']
        new = list(filter(None, new))
        for i in new:
            word = i.split(' ')
            master.extend(word)
        # Cleans empty values to return a list of words
        for i in master:
            if i != '':
                final.append(i)
        for a in final:
            # Matches words to regex and if it still contains script parameters get's rid of them
            extract = re.compile('[a-zA-Z\'-]+')
            clean = re.sub(extract,'',a)
            if len(clean) == 0 and a not in elements:
                FINAL.append(a)
        return FINAL

    @classmethod
    def get_density(self,keyword,body):
        data = {}
        print(keyword)
        ngram = []
        clean = keyword.split(' ')
        lengthKeyword = len(clean)
        data['content_length'] = len(body)
        counter = 0
        for i in range(len(body)):
            ngram.append(body[counter:counter + lengthKeyword])
            counter = counter + 1
        wordList = []
        for i in ngram:
            new = ' '.join(i)
            wordList.append(new)
        count = 0
        for a in wordList:
            if a.lower() == keyword:
                count += 1
            else:
                continue
        try:
            Density = count / len(body)
            data['density'] = Density
        except:
            Density = None
            data['density'] = Density
        data['keyword_mentions'] = count
        return data


class META():
    data = {}

    def __init__(self, url, body):
        print(url)
        soup = BeautifulSoup(body)
        self.url = url
        self.now = time.strftime('%Y-%m-%d %H:%M')
        try:
            gen = soup.find('meta', attrs={'name': 'generator'})
            self.type1 = 'none'
            if gen['content'] is not None:
                self.type1 = gen['content']
            self.now = time.strftime('%Y-%m-%d %H:%M')
        except:
            self.type1 = 'None'
        try:
            self.meta_title = soup.title.text
            self.title_length = len(self.meta_title)
        except:
            self.meta_title = 'N/A'
            self.title_length = 'N/A'
        try:
            meta_description = soup.find('meta', attrs={'name': 'description'})
            self.meta_description = meta_description['content']
            self.meta_description_length = len(meta_description)
        except:
            self.meta_description = 'N/A'
            self.meta_description_length = 'N/A'
        try:
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            self.canonical_count = len(soup.findAll('link', attrs={'rel': 'canonical'}))
            self.canonical = canonical['href']
        except:
            self.canonical = 'N/A'
            self.canonical_count = 0
        try:
            robots = soup.find('meta', attrs={'name': 'robots'})
            self.robots = robots['content']
        except:
            self.robots = 'N/A'
        try:
            self.H1 = soup.find('h1').text
        except:
            self.H1 = 'None'
