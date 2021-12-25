from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'keep-alive',
    'DNT':'1'
}

button_next_auto = InlineKeyboardMarkup().add(InlineKeyboardButton("Следующий автомобиль", callback_data="next_auto"))


def parse_site(page):
    site_content = session.get('https://auto.ru/cars/nissan/all/?page={page}&output_type=carousel', headers=headers)
    site_content = session.get('https://auto.ru/cars/nissan/all/?page={page}&output_type=carousel', headers=headers)
    site_content.encoding = 'utf-8'
    site_content = BeautifulSoup(site_content.text, 'lxml')
    
    output = []
    cars = [el for el in site_content.find_all('div', class_="ListingItemWide")]
    if len(cars) > 0:
        output.append('Нашёл для тебя прекрасную подборку автомобилей😄')
    else:
        return ['К сожелению подборка пуста😔']
        
    for car in cars:
        name = car.h3.text
        cost = car.find('div', class_='ListingItemPrice__content').span.text
        link = car.a['href']
        output.append(f'\n Название: {name} \nЦена: {cost} \nСсылка: {link}')
    
    return output


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
session = requests.Session()
session.get('https://auto.ru', headers=headers)

cars = []
cnt = 1

@dp.message_handler(commands=['refresh'])
async def parse(message: types.Message):
    global cars, cnt
    cnt = 1
    cars = parse_site(cnt)
    await bot.send_message(message.from_user.id, cars[0])
    cars = cars[1:]
    if (len(cars) == 0):
        return
    car = cars.pop()
    await bot.send_message(message.from_user.id, car, reply_markup=button_next_auto)
    
@dp.callback_query_handler()
async def next_auto_function(callback_query: types.CallbackQuery):
    global cars, cnt
    if (callback_query.data == 'next_auto'):
        if (len(cars) == 0):
            cnt+=1
            cars = parse_site(cnt)[1:]
            if (len(cars) == 0):
                await bot.send_message(callback_query.from_user.id, 'Автомобили в подборке закончились')
                return
        
        car = cars.pop()
        await callback_query.message.edit_text(car, reply_markup=button_next_auto)


if __name__== "__main__":
    executor.start_polling(dp, skip_updates=True)