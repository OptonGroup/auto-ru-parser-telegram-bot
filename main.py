from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from config import URL
from autorucars import autorucars

button_next_auto = InlineKeyboardMarkup().add(InlineKeyboardButton("Следующий автомобиль", callback_data="next_auto"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

cars = set()

@dp.message_handler(commands=['refresh'])
async def parse(message: types.Message):
    global cars
    cars = autorucars(URL)
    
    car = cars.next_car()
    file = open('index.html', 'w', encoding='utf-8')
    file.write(str(car))
    file.close()
    await bot.send_document(message.from_user.id, open('index.html', 'rb'))
    return
    while 1:
        if (car == False):
            break
        if (len(car) == 7):
            break
        car = cars.next_car()
    if car != False:
        await bot.send_message(message.from_user.id, 'Нашёл для тебя прекрасную подборку автомобилей😄')
        await bot.send_message(message.from_user.id, f'Название: {car[2]}\nЦена: {car[3]}₽\nСсылка: {car[1]}', reply_markup=button_next_auto)
    else:
        await bot.send_message(message.from_user.id, 'К сожелению подборка пуста😔')
    
@dp.callback_query_handler()
async def next_auto_function(callback_query: types.CallbackQuery):
    if (callback_query.data == 'next_auto'):
        if (cars == set()):
            await callback_query.message.edit_text('Пропишите /refresh ещё раз')
            return
        car = cars.next_car()
        while 1:
            if (car == False):
                break
            if (len(car) == 7):
                break
            car = cars.next_car()
        if car != False:
            await callback_query.message.edit_text(f'Название: {car[2]}\nЦена: {car[3]}₽\nСсылка: {car[1]}', reply_markup=button_next_auto)
        else:
            await callback_query.message.edit_text('Автомобили в подборке закончились')


if __name__== "__main__":
    executor.start_polling(dp, skip_updates=True)