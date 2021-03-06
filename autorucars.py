from requests import Session
from bs4 import BeautifulSoup
from json import loads
import time

class autorucars(object):
    def __init__(self, url):
        self.url = url
        self.watched_cars = set()
        self.cars = {}
        self.page = 0
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36',
            'X-Vertis-DC': 'sas', 
            '_csrf_token': 'b5786b636d5f917e627ae283752eba1ad571de035d608018', 
            '_yasc': 'YE+88d2U9TsCDLTnhSXo3F2BJrz5JPWQvg4tg+wokCKhlg==', 
            'from': 'direct', 
            'from_lifetime': '1640583649237', 
            'suid': 'd1e72614fba7f20abd76bdde07f4d8db.0ad38b80a0db1bcc713eba2d0bcddbd0'
        }
        self.max_page = -1

    def __next_page(self):
        session = Session()
        response = session.get(url=self.url+str(self.page), headers=self.headers)
        response.encoding = 'utf-8'
        return set([response.text])
        cars_json = loads(BeautifulSoup(response.text, 'lxml').find('script').text)['offers']['offers']
        cars = set(tuple(el.values()) for el in cars_json)

        if (self.max_page == -1):
            max_page = BeautifulSoup(response.text, 'lxml').find_all('a', class_='ListingPagination__page')
            if (max_page):
                self.max_page = max_page[-1].text
            else:
                self.max_page = 1
        
        cars -= self.watched_cars
        self.watched_cars |= cars
        return cars

    def next_car(self):
        if (len(self.cars) == 0):
            self.page += 1
            if (self.max_page != -1 and self.page > self.max_page):
                return False
            self.cars = self.__next_page()
            if (len(self.cars) == 0):
                return False
        
        return self.cars.pop()