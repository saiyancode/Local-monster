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
        self.body = self.clean_page(body)
        result = self.get_density(keyword[0],self.body)
        print(result)

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
        print(keyword)
        ngram = []
        clean = keyword.split(' ')
        lengthKeyword = len(clean)
        print(lengthKeyword)
        print(len(body))
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
        except:
            Density = None
        return Density


class meta_data():
    data = {}

    def __init__(self, url, body, Project, cursor, db):
        soup = BeautifulSoup(body)
        self.url = url
        self.project = Project
        try:
            gen = soup.find('meta', attrs={'name': 'generator'})
            type1 = 'none'
            if gen['content'] is not None:
                type1 = gen['content']
            self.now = time.strftime('%Y-%m-%d %H:%M')
            # cursor.execute('''INSERT INTO results(id,url,type,time)
            #                   VALUES(?,?,?,?)''', (Project, url, type1, self.now))
            # db.commit()
        except:
            type1 = 'None'
            self.now = time.strftime('%Y-%m-%d %H:%M')
            # cursor.execute('''INSERT INTO results(id,url,type,time)
            #                           VALUES(?,?,?,?)''', (Project, url, type1, self.now))
            # db.commit()
        try:
            meta_title = soup.title.text
            title_length = len(meta_title)
        except:
            meta_title = 'N/A'
            title_length = 'N/A'
        try:
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description['content']
            meta_description_length = len(meta_description)
        except:
            meta_description = 'N/A'
            meta_description_length = 'N/A'
        try:
            response_header = response_header
        except:
            response_header = 'N/A'
        try:
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            canonical_count = len(soup.findAll('link', attrs={'rel': 'canonical'}))
            canonical = canonical['href']
            canonical_count = canonical_count
        except:
            canonical = 'N/A'
            canonical_count = 0
        try:
            robots = soup.find('meta', attrs={'name': 'robots'})
            robots = robots['content']
        except:
            robots = 'N/A'

        cursor.execute('''INSERT INTO results(id,url,meta_title,title_length,meta_description,description_length,
        response_header,canonical,canonical_count,robots,type,time)
                                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', (Project, url, meta_title,
                                                                                   title_length, meta_description,
                                                                                   meta_description_length,
                                                                                   response_header, canonical,
                                                                                   canonical_count, robots, type1,
                                                                                   self.now))
        db.commit()