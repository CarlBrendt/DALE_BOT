<<<<<<< HEAD
'''
import asyncio
import logging
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from config_reader import config
from app.description_constuctor_handler import router
from main_router import main_router
from app.middleware import TestMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from bot_instance import BotManager
from aiogram import types, F, Router
from aiogram.types import Message, ContentType
from aiogram.filters.command import Command
from app.states import UserState
from aiogram.fsm.context import FSMContext
import app.keyboard as kb
from random import choice
from config_reader import config




PRICE_FOR_DESCRIPTION = types.LabeledPrice(label='Сгенерировать описание', amount=20*100) # цена в копейках
TEST_TOKEN = config.payment_token.get_secret_value()

@dp.message(Command('status'))
async def check(message: Message, state: FSMContext):
    
        await bot.send_invoice(message.chat.id,
                            title = 'Сгенерировать описание',
                            description = 'Оплата генерации одного описания',
                            provider_token=TEST_TOKEN,
                            is_flexible = False,
                            price = [PRICE_FOR_DESCRIPTION],
                            start_parameter='one_description_payment',
                            payload='test-invoice-payload')
        
# Делаем пречекаут прежде чем пользователь оплатит покупку. Можем проверить наличие товара на складе перед оплатой
# ВАЖНО дать ответ серверу телеграма в течение 10 секунд
@dp.pre_checkout_query(lambda query: True)
async def handle_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)
    
# Выводим каку-то информацию после того как платеж был совершен
# здесь можно отправлять информацию менеджеру
@dp.message(types.successful_payment.SuccessfulPayment)
async def handle_successful_payment(message: Message, state: FSMContext):
        data = await state.get_data()
        number_of_rooms = data.get('number_of_rooms', 'не указано')
        renovation_status = data.get('renovation_status', 'не указано')
        style = data.get('style', 'не указано')
        kitchen_living_room = data.get('kitchen_living_room', 'не указано')
        number_of_closet = data.get('number_of_closet', 'не указано')
        bed_count = data.get('number_of_bedrooms', 'не указано')
        flat_view = data.get('flat_view', 'не указано')
        flat_area = data.get('flat_area', 'не указано')
        price = data.get('price', 'не указано')
        price_int = data.get('price_int', 'не указано')
        flat_details = data.get('flat_details', 'не указано')
        link_house = data.get('link_house', 'не указано')

        if bed_count != 'не указано':
            try:
                bed_count = int(bed_count)
            except ValueError:
                await message.answer("Некорректное значение количества спален.")
                return
            
            bedrooms_info = []
            for i in range(1, bed_count + 1):
                area = data.get(f'bedroom_{i}_area', 'не указано')
                wc = data.get(f'bedroom_{i}_wc', 'не указано')
                bed_type = data.get(f'bedroom_{i}_type', 'не указано')
                bed_view = data.get(f'bedroom_{i}_view', 'не указано')
                bed_details = data.get(f'bedroom_{i}_details', 'не указано')
                bedrooms_info.append(f"Спальня {i}: Площадь - {area}, Санузел - {wc}, Тип - {bed_type}, Вид - {bed_view}, Детали - {bed_details}")

            bedrooms_info_str = "\n".join(bedrooms_info)
        else:
            bedrooms_info_str = "Количество спален не указано."

        await message.answer(
            f"В вашей квартире {number_of_rooms}, она {renovation_status}, стиль: {style}, кухня совмещена с гостиной: {kitchen_living_room}, количество санузлов: {number_of_closet}, количество спален: {bed_count}, "
            f"вид из окон: {flat_view}, общая площадь: {flat_area}, цена: {price} {price_int}, достоинства: {flat_details}, ссылка на ЖК: {link_house}\n\n"
            f"Информация о спальнях:\n{bedrooms_info_str}"
        )
'''
=======
'''
import asyncio
import logging
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from config_reader import config
from app.description_constuctor_handler import router
from main_router import main_router
from app.middleware import TestMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from bot_instance import BotManager
from aiogram import types, F, Router
from aiogram.types import Message, ContentType
from aiogram.filters.command import Command
from app.states import UserState
from aiogram.fsm.context import FSMContext
import app.keyboard as kb
from random import choice
from config_reader import config




PRICE_FOR_DESCRIPTION = types.LabeledPrice(label='Сгенерировать описание', amount=20*100) # цена в копейках
TEST_TOKEN = config.payment_token.get_secret_value()

@dp.message(Command('status'))
async def check(message: Message, state: FSMContext):
    
        await bot.send_invoice(message.chat.id,
                            title = 'Сгенерировать описание',
                            description = 'Оплата генерации одного описания',
                            provider_token=TEST_TOKEN,
                            is_flexible = False,
                            price = [PRICE_FOR_DESCRIPTION],
                            start_parameter='one_description_payment',
                            payload='test-invoice-payload')
        
# Делаем пречекаут прежде чем пользователь оплатит покупку. Можем проверить наличие товара на складе перед оплатой
# ВАЖНО дать ответ серверу телеграма в течение 10 секунд
@dp.pre_checkout_query(lambda query: True)
async def handle_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)
    
# Выводим каку-то информацию после того как платеж был совершен
# здесь можно отправлять информацию менеджеру
@dp.message(types.successful_payment.SuccessfulPayment)
async def handle_successful_payment(message: Message, state: FSMContext):
        data = await state.get_data()
        number_of_rooms = data.get('number_of_rooms', 'не указано')
        renovation_status = data.get('renovation_status', 'не указано')
        style = data.get('style', 'не указано')
        kitchen_living_room = data.get('kitchen_living_room', 'не указано')
        number_of_closet = data.get('number_of_closet', 'не указано')
        bed_count = data.get('number_of_bedrooms', 'не указано')
        flat_view = data.get('flat_view', 'не указано')
        flat_area = data.get('flat_area', 'не указано')
        price = data.get('price', 'не указано')
        price_int = data.get('price_int', 'не указано')
        flat_details = data.get('flat_details', 'не указано')
        link_house = data.get('link_house', 'не указано')

        if bed_count != 'не указано':
            try:
                bed_count = int(bed_count)
            except ValueError:
                await message.answer("Некорректное значение количества спален.")
                return
            
            bedrooms_info = []
            for i in range(1, bed_count + 1):
                area = data.get(f'bedroom_{i}_area', 'не указано')
                wc = data.get(f'bedroom_{i}_wc', 'не указано')
                bed_type = data.get(f'bedroom_{i}_type', 'не указано')
                bed_view = data.get(f'bedroom_{i}_view', 'не указано')
                bed_details = data.get(f'bedroom_{i}_details', 'не указано')
                bedrooms_info.append(f"Спальня {i}: Площадь - {area}, Санузел - {wc}, Тип - {bed_type}, Вид - {bed_view}, Детали - {bed_details}")

            bedrooms_info_str = "\n".join(bedrooms_info)
        else:
            bedrooms_info_str = "Количество спален не указано."

        await message.answer(
            f"В вашей квартире {number_of_rooms}, она {renovation_status}, стиль: {style}, кухня совмещена с гостиной: {kitchen_living_room}, количество санузлов: {number_of_closet}, количество спален: {bed_count}, "
            f"вид из окон: {flat_view}, общая площадь: {flat_area}, цена: {price} {price_int}, достоинства: {flat_details}, ссылка на ЖК: {link_house}\n\n"
            f"Информация о спальнях:\n{bedrooms_info_str}"
        )
'''
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
