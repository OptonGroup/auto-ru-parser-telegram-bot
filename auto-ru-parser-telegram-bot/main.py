from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import requests
from bs4 import BeautifulSoup
from config import TOKEN
import json

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36'
}

file = open('json.json', 'w', encoding='utf-8')

def get_content(url):
    session = requests.Session()
    response = session.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    json_text = json.loads(BeautifulSoup(response.text, 'lxml').find('script').text)
    file.write(str(json_text['offers']['offers']))
    file.write('\n\n\n')
    
        

def main():
    pages = 
    get_content(url='https://auto.ru/cars/nissan/all/?page=1&output_type=carousel')
    get_content(url='https://auto.ru/cars/nissan/all/?page=2&output_type=carousel')
    get_content(url='https://auto.ru/cars/nissan/all/?page=3&output_type=carousel')

if __name__== "__main__":
    main()
    
# button_next_auto = InlineKeyboardMarkup().add(InlineKeyboardButton("Следующий автомобиль", callback_data="next_auto"))