from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from app.states import UserState
from aiogram.fsm.context import FSMContext
import keyboard.keyboard as kb
from random import choice
import asyncio
import re
from app.description_constructor.description_with_gpt import create_unique_description_of_building # асинхронная функция для преобразования gpt
from app.description_constructor.description_with_gpt import create_description_of_flat
router = Router()

class DescriptionConstructorHandler:
    
    # асинхронно вызываем функцию для создания описания жк с gpt
    @staticmethod
    async def uniquely_describe_building(info: str, extra_info: str, state: FSMContext):
        try:
            # Убедитесь, что info содержит необходимую информацию
            if not info:
                unique_text = "Информация о ЖК не указана."
            else:
                unique_text = await create_unique_description_of_building(info, extra_info)
            
            await state.update_data(unique_description_of_building=unique_text)
        except Exception as e:
            await state.update_data(unique_description_of_building=f"Ошибка при создании описания: {str(e)}")

    # асинхронно вызываем функцию для создания описания квартиры с gpt
    @staticmethod
    async def create_unique_description_of_flat(flat_info: str, jk_info: str, state: FSMContext):
        try:
            flat_text = await create_description_of_flat(flat_info, jk_info)
            await state.update_data(flat_text=flat_text)
            
            # Смена состояния после завершения создания описания
            await state.set_state(UserState.description_ready)

        except Exception as e:
            await state.update_data(flat_text=f"Ошибка при создании описания: {str(e)}")

    # Функция которая возвращает информаци от пользователя чтобы мы передали ее в функции для генерации описания
    @staticmethod
    async def collect_info_from_fsm(state: FSMContext):
        data = await state.get_data()
        responses = [
            f"Количество комнат в квартире: {data.get('number_of_rooms', 'не указано')}",
            f"Состояние ремонта: {data.get('renovation_status', 'не указано')}",
            f"Стиль квартиры: {data.get('style', 'не указано')}",
            f"Кухня совмещена с гостиной: {data.get('kitchen_living_room', 'не указано')}",
            f"Количество санузлов: {data.get('number_of_closet', 'не указано')}",
            f"Количество спален: {data.get('number_of_bedrooms', 'не указано')}",
        ]

        if data.get('number_of_bedrooms', 0) > 0:
            bed_count = int(data.get('number_of_bedrooms', 0))
            bedrooms_info = [
                f"Спальня {i + 1}: Площадь - {data.get(f'bedroom_{i+1}_area', 'не указано')}, Санузел - {data.get(f'bedroom_{i+1}_wc', 'не указано')}, Тип - {data.get(f'bedroom_{i+1}_type', 'не указано')}, Вид - {data.get(f'bedroom_{i+1}_view', 'не указано')}, Детали - {data.get(f'bedroom_{i+1}_details', 'не указано')}" 
                for i in range(bed_count)
            ]
            responses.append("Информация о спальнях:\n" + "\n".join(bedrooms_info))
        else:
            responses.append("Информация о спальнях не указана.")

        responses.extend([
            f"Виды из окон квартиры: {data.get('flat_view', 'не указано')}",
            f"Общая площадь квартиры: {data.get('flat_area', 'не указано')}",
            f"Валюта цены: {data.get('price', 'не указано')}",
            f"Цена квартиры: {data.get('price_int', 'не указано')}",
            f"Достоинства и плюсы квартиры: {data.get('flat_details', 'не указано')}",
            f"Дополнительные комнаты в квартире: {data.get('info_about_extra_rooms', 'не указано')}",
            f"Обязательная информация о квартире: {data.get('flat_extra_info', 'не указано')}",
            f"Описание жк: {data.get('unique_description_of_building', 'не указано')}",
            f"Условия сделки: {data.get('deal_term', 'не указано')}"
        ])
        
        flat_info = "\n".join(responses)  # Собираем информацию о квартире
        jk_info = responses[-2]  # Информация о ЖК
        return flat_info, jk_info  # Возвращаем оба текста

    # Хендлер Конструктора описания и видео о квартире
    @staticmethod
    @router.message(F.text.in_(["Конструктор описания квартиры", "Сформировать видео о квартире"]))
    async def handle_catch_cian(message: Message, state: FSMContext):
        if message.text == "Конструктор описания квартиры":
            await state.clear()
            await message.answer('Вы выбрали конструктор описания квартиры. Ответьте на несколько вопросов и я пришлю вам красочное описание квартиры💫\n\n*Note:*\nВ любой момент вы можете посмотреть всю информацию, которую ввели ранее.\nДля этого в меню выберите режим /status', 
                                parse_mode='Markdown',
                                reply_markup=await kb.Custom_Keyboard().agree_keyboard())
        elif message.text == 'Сформировать видео о квартире':
            await message.answer('Вы выбрали сформировать видео из картинок для квартиры. Выберите сколько фото вы хотите прислать')

    # Ловим согласие пользователя на создание описания комнаты
    @staticmethod
    @router.callback_query(F.data.in_(['I_agree']))
    async def handle_agreement(callback: CallbackQuery, state: FSMContext):
        await callback.message.edit_text('Пожалуйста выберите количество комнат в квартире', reply_markup=await kb.Custom_Keyboard().rooms_select_keyboard())
        await state.set_state(UserState.number_of_rooms)
        await state.update_data(last_question='Пожалуйста выберите количество комнат в квартире')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().rooms_select_keyboard())

    # Ловим количество комнат пользователей и записываем в FSM
    @staticmethod
    @router.callback_query(UserState.number_of_rooms, F.data.in_(['one_room', 'two_rooms', 'three_rooms', 'many_rooms', 'empty', 'studio', 'rooms_backs']))
    async def handle_number_of_rooms(callback: CallbackQuery, state: FSMContext):
        room_map = {
            'one_room': '1 комната',
            'two_rooms': '2 комнаты',
            'three_rooms': '3 комнаты'
        }
        if callback.data in room_map:
            await state.update_data(number_of_rooms=room_map[callback.data])
            await state.set_state(UserState.renovation_status)
            await state.update_data(last_question='Квартира с отделкой или без?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().select_renovation_keyboard())
            await callback.message.answer('Квартира с отделкой или без?', reply_markup=await kb.Custom_Keyboard().select_renovation_keyboard())
        
        elif callback.data == 'many_rooms':
            await callback.message.answer('Пожалуйста, введите сколько в вашей квартире комнат\n Формат и пример ввода: 6\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.set_state(UserState.waiting_for_room_count)
            await state.update_data(last_question='Пожалуйста, введите сколько в вашей квартире комнат\n Формат и пример ввода: 6\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
        elif callback.data == 'empty':
            await state.update_data(number_of_rooms='В квартире свободная планировка')
            await state.set_state(UserState.flat_view)
            await state.update_data(last_question='Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинускую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await callback.message.answer('Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинускую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        elif callback.data == 'studio':
            await state.update_data(number_of_rooms='Квартира студия')
            await state.set_state(UserState.renovation_status)
            await state.update_data(last_question='Квартира с отделкой или без?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().select_renovation_keyboard())
            await callback.message.answer('Квартира с отделкой или без?', reply_markup=await kb.Custom_Keyboard().select_renovation_keyboard())
        
        elif callback.data == "rooms_backs":
            await callback.message.answer('Вы выбрали конструктор описания квартиры. Ответьте на несколько вопросов и я пришлю вам красочное описание квартиры', 
                                            reply_markup=await kb.Custom_Keyboard().agree_keyboard())
            await state.clear()

    # Ловим количество комнат и записываем в состояние комнат
    @staticmethod
    @router.message(UserState.waiting_for_room_count)
    async def handle_room_count(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        room_count = message.text
        await state.update_data(number_of_rooms=f'{room_count} комнат')
        await state.set_state(UserState.renovation_status)
        await state.update_data(last_question='Квартира с отделкой или без?')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().select_renovation_keyboard())
        await message.answer('Квартира с отделкой или без?', reply_markup=await kb.Custom_Keyboard().select_renovation_keyboard())

    @staticmethod
    @router.callback_query(UserState.renovation_status, F.data.in_(['with_renovation', 'no_renovation', 'renovation_backs']))
    async def handle_renovation_status(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'with_renovation':
            await state.update_data(renovation_status='Квартира с отделкой')
            await state.set_state(UserState.style)
            await state.update_data(last_question='Пожалуйста введи стиль, в котором оформлена ваша квартира\n\nПримеры:\n1 пример - модерн\n2 пример - моя квартира в стиле eclectic\n3 пример - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await callback.message.answer('Пожалуйста введи стиль, в котором оформлена ваша квартира\n\nПримеры:\n1 пример - модерн\n2 пример - моя квартира в стиле eclectic\n3 пример - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        elif callback.data == 'no_renovation':
            await state.update_data(renovation_status='Квартира без отделки')
            data = await state.get_data()
            if data['number_of_rooms'] != 'Квартира студия':
                await state.set_state(UserState.kitchen_living_room)
                await state.update_data(last_question='Кухня совмещена с гостиной?')
                await state.update_data(last_keyboard=await kb.Custom_Keyboard().kitchen_with_living_room_keyboard())
                await callback.message.answer('Кухня совмещена с гостиной?', reply_markup=await kb.Custom_Keyboard().kitchen_with_living_room_keyboard())
            else:
                await state.set_state(UserState.flat_view)
                await state.update_data(last_question='Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинскую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
                await state.update_data(last_keyboard=None)
                await callback.message.answer('Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинскую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        
        elif callback.data == 'renovation_backs':
            await callback.message.answer('Пожалуйста выберите количество комнат в квартире', reply_markup=await kb.Custom_Keyboard().rooms_select_keyboard())
            await state.set_state(UserState.number_of_rooms)
            await state.update_data(last_question='Пожалуйста выберите количество комнат в квартире')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().rooms_select_keyboard())
            
    @staticmethod
    @router.message(UserState.style)
    async def handle_style(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(style=f"Стиль квартиры {message.text}")
        data = await state.get_data()
        if data['number_of_rooms']!='Квартира студия':
            await state.set_state(UserState.kitchen_living_room)
            await state.update_data(last_question='Кухня совмещена с гостиной?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().kitchen_with_living_room_keyboard())
            await message.answer('Кухня совмещена с гостиной?', reply_markup=await kb.Custom_Keyboard().kitchen_with_living_room_keyboard())
        else:
            await state.set_state(UserState.flat_view)
            await state.update_data(last_question='Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинскую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await message.answer('Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинускую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        
    # Ловим статус совмещения кухни с гостиной
    @staticmethod
    @router.callback_query(UserState.kitchen_living_room, F.data.in_(['yes_single_room', 'no_single_room', 'single_room_back']))
    async def handle_kitchen_with_living_room_status(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'yes_single_room':
            await state.update_data(kitchen_living_room='В квартире совмещены кухня и гостиная')
        elif callback.data == 'no_single_room':
            await state.update_data(kitchen_living_room='Кухня и гостиная две разные комнаты')
        elif callback.data == 'single_room_back':
            await state.set_state(UserState.renovation_status)
            await state.update_data(last_question='Квартира с отделкой или без?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().select_renovation_keyboard())
            await callback.message.answer('Квартира с отделкой или без?', reply_markup=await kb.Custom_Keyboard().select_renovation_keyboard())
            return

        await state.set_state(UserState.number_of_closet)
        await state.update_data(last_question='Сколько санузлов во ВСЕЙ квартире?')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().wc_select_keyboard())
        await callback.message.answer('Сколько санузлов во ВСЕЙ квартире?', reply_markup=await kb.Custom_Keyboard().wc_select_keyboard())

    @staticmethod
    # Ловим количество санузлов и записываем в FSM
    @router.callback_query(UserState.number_of_closet, F.data.in_(['one_wc', 'two_wc', 'three_wc', 'many_wc', 'wc_backs']))
    async def handle_number_of_closets(callback: CallbackQuery, state: FSMContext):
        wc_map = {
            'one_wc': '1 санузел',
            'two_wc': '2 санузла',
            'three_wc': '3 санузла'
        }
        if callback.data in wc_map:
            await state.update_data(number_of_closet=f"В квартире {wc_map[callback.data]}")
            await callback.message.answer('Сколько спален в вашей квартире?',reply_markup=await kb.Custom_Keyboard().bedroom_select_keyboard())
            await state.set_state(UserState.number_of_bedrooms)
            await state.update_data(last_question='Сколько спален в вашей квартире?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().bedroom_select_keyboard())
        elif callback.data == 'many_wc':
            await callback.message.answer('Пожалуйста, введите сколько в вашей квартире санузлов\nФормат и пример ввода: 6\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ !!')
            await state.set_state(UserState.waiting_for_closet_count)
            await state.update_data(last_question='Пожалуйста, введите сколько в вашей квартире санузлов\nФормат и пример ввода: 6\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
        elif callback.data == "wc_backs":
            await callback.message.answer('Кухня совмещена с гостиной?', reply_markup=await kb.Custom_Keyboard().kitchen_with_living_room_keyboard())
            await state.set_state(UserState.kitchen_living_room)
            await state.update_data(last_question='Кухня совмещена с гостиной?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().kitchen_with_living_room_keyboard())

    # Ловим количество санузлов и записываем в состояние санузлов
    @staticmethod
    @router.message(UserState.waiting_for_closet_count)
    async def handle_closet_count(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        wc_count = message.text
        await state.update_data(number_of_closet=f'В квартире {wc_count} санузлов')
        await state.set_state(UserState.number_of_bedrooms) # говорим что сейчас будем ловить информацию о количествах спальней
        await state.update_data(last_question='Сколько спален в вашей квартире?')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().bedroom_select_keyboard())
        await message.answer('Сколько спален в вашей квартире?',reply_markup=await kb.Custom_Keyboard().bedroom_select_keyboard())

    # Ловим количество спален и записываем в FSM
    @staticmethod
    @router.callback_query(UserState.number_of_bedrooms, F.data.in_(['one_bed', 'two_bed', 'three_bed', 'many_bed', 'bed_backs']))
    async def handle_number_of_bedrooms(callback: CallbackQuery, state: FSMContext):
        bed_map = {
            'one_bed': '1 спальня',
            'two_bed': '2 спальни',
            'three_bed': '3 спальни'
        }
        if callback.data in bed_map:
            await state.update_data(number_of_bedrooms=int(bed_map[callback.data].split()[0]))
            await state.update_data(current_bed=1)
            await state.set_state(UserState.info_bed)
            await state.update_data(last_question='Теперь ответьте на несколько вопросов о КАЖДОЙ спальне')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().agree_keyboard_about_bed())
            await callback.message.answer('Теперь ответьте на несколько вопросов о КАЖДОЙ спальне', reply_markup=await kb.Custom_Keyboard().agree_keyboard_about_bed())
        elif callback.data == 'many_bed':
            await callback.message.answer('Пожалуйста, введите сколько в вашей квартире спален\nФормат и пример ввода: 6\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.set_state(UserState.waiting_for_bedrooms_count)
            await state.update_data(last_question='Пожалуйста, введите сколько в вашей квартире спален\nФормат и пример ввода: 6\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
        elif callback.data == "bed_backs":
            await callback.message.answer('Сколько санузлов во ВСЕЙ квартире?', reply_markup=await kb.Custom_Keyboard().wc_select_keyboard())
            await state.set_state(UserState.number_of_closet)
            await state.update_data(last_question='Сколько санузлов во ВСЕЙ квартире?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().wc_select_keyboard())
            await state.update_data(last_keyboard=None)
    # Обработчик для ввода количества спален через клавиатуру
    @staticmethod
    @router.message(UserState.waiting_for_bedrooms_count)
    async def handle_bedroom_count(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        try:
            bed_count = int(message.text)
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число спален.")
            return
        await state.update_data(number_of_bedrooms=bed_count)
        await state.update_data(current_bed=1)
        await state.set_state(UserState.info_bed)
        await state.update_data(last_question='Теперь ответьте на несколько вопросов о КАЖДОЙ спальне')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().agree_keyboard_about_bed())
        await message.answer('Теперь ответьте на несколько вопросов о КАЖДОЙ спальне', reply_markup=await kb.Custom_Keyboard().agree_keyboard_about_bed())

    # Обработчик начала ввода информации о каждой спальне
    @staticmethod
    @router.callback_query(UserState.info_bed, F.data=='got_it')
    async def handle_info_about_beds(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        current_bed = data.get('current_bed', 1)
        await state.set_state(UserState.bedroom_area)
        await state.update_data(last_question=f'Расскажите какая площадь вашей * {current_bed} * спальни\n\nПример 1: 20,2\nПример 2: 12\nПример 3: Не знаю площадь\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await callback.message.answer(f'Расскажите какая площадь вашей * {current_bed} * спальни\n\nПример 1: 20,2\nПример 2: 12\nПример 3: Не знаю площадь\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')

    # Обработчик для ввода информации о площади спальни
    @staticmethod
    @router.message(UserState.bedroom_area)
    async def handle_bedroom_area(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        data = await state.get_data()
        current_bed = data.get('current_bed', 1)

        # Сохраняем площадь текущей спальни
        await state.update_data(**{f'bedroom_{current_bed}_area': message.text})

        await state.set_state(UserState.bedroom_wc)
        await state.update_data(last_question='В этой спальне свой санузел?')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().number_of_wc_in_bedroom())
        await message.answer('В этой спальне свой санузел?', reply_markup=await kb.Custom_Keyboard().number_of_wc_in_bedroom())

    # Обработчик для ввода информации о санузле в спальне
    @staticmethod
    @router.callback_query(UserState.bedroom_wc, F.data.in_(['yes_wc_bed', 'no_wc_bed', 'wc_bed_back']))
    async def handle_wc_info(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        current_bed = data.get('current_bed', 1)

        if callback.data == 'wc_bed_back':
            await state.set_state(UserState.bedroom_area)
            await state.update_data(last_question=f'Расскажите какая площадь спальни {current_bed}\n\nПример 1: 20,2\nПример 2: 12\nПример 3: Не знаю площадь\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await callback.message.answer(f'Расскажите какая площадь спальни {current_bed}\n\nПример 1: 20,2\nПример 2: 12\nПример 3: Не знаю площадь\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            return

        wc_status = 'свой санузел' if callback.data == 'yes_wc_bed' else 'нет своего санузла'

        # Сохраняем информацию о санузле текущей спальни
        await state.update_data(**{f'bedroom_{current_bed}_wc': wc_status})
        await state.set_state(UserState.bedroom_type)
        await state.update_data(last_question='Какой тип этой спальни?')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().type_of_bedroom())
        await callback.message.answer('Какой тип этой спальни?', reply_markup=await kb.Custom_Keyboard().type_of_bedroom())

    # Обработчик для ввода информации о типе конкретной спальни
    @staticmethod
    @router.callback_query(UserState.bedroom_type,  F.data.in_(['master', 'guest', 'kids', 'type_back']))
    async def handle_type_info(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        current_bed = data.get('current_bed', 1)
        
        if callback.data == 'type_back':
            await state.set_state(UserState.bedroom_wc)
            await state.update_data(last_question='В этой спальне свой санузел?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().number_of_wc_in_bedroom())
            await callback.message.answer('В этой спальне свой санузел?', reply_markup=await kb.Custom_Keyboard().number_of_wc_in_bedroom())
            return

        if callback.data == 'master':
            type_status = 'Мастер спальня'
        elif callback.data == 'guest':
            type_status = 'Гостевая спальня'
        else:
            type_status = 'Детская спальня'

        # Сохраняем информацию о типе текущей спальни
        await state.update_data(**{f'bedroom_{current_bed}_type': type_status})
        await state.set_state(UserState.bedroom_view)
        await state.update_data(last_question='Опишите вид из этой спальни\n\nПример ввода:\nПример 1 - Вид на парк Горького, панорамные окна, Парк как на ладони, солнечная сторона\nПример 2 - Окна выходят в тихий зеленый двор, видна парковка\nПример 3 - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await callback.message.answer('Опишите вид из этой спальни\n\nПример ввода:\nПример 1 - Вид на парк Горького, панорамные окна, Парк как на ладони, солнечная сторона\nПример 2 - Окна выходят в тихий зеленый двор, видна парковка\nПример 3 - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')

    # Обработчик для ввода информации о виде из спальни
    @staticmethod
    @router.message(UserState.bedroom_view)
    async def handle_view_from_bedroom(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        data = await state.get_data()
        current_bed = data.get('current_bed', 1)
        bed_count = data.get('number_of_bedrooms', 1)

        # Сохраняем вид из текущей спальни
        await state.update_data(**{f'bedroom_{current_bed}_view': message.text})
        await state.set_state(UserState.bedroom_details)
        await state.update_data(last_question='Расскажите мне немного об интересных деталях этой спальни\n\nПример 1 - Дизайнерский ремонт, встроенные зеркала ручной работы\nПример 2 - нет\nПример 3 - умное освещение и кондиционер, фильтрация воздуха\nПример 4 - не знаю ничего о деталях\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await message.answer('Расскажите мне немного об интересных деталях этой спальни\n\nПример 1 - Дизайнерский ремонт, встроенные зеркала ручной работы\nПример 2 - нет\nПример 3 - умное освещение и кондиционер, фильтрация воздуха\nПример 4 - не знаю ничего о деталях\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')

    @staticmethod
    @router.message(UserState.bedroom_details)
    async def handle_view_from_bedroom(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        data = await state.get_data()
        current_bed = data.get('current_bed', 1)
        bed_count = data.get('number_of_bedrooms', 1)

        # Сохраняем вид из текущей спальни
        await state.update_data(**{f'bedroom_{current_bed}_details': message.text})

        if current_bed < bed_count: # сравниваем счетчик с реальным количеством спален
            current_bed += 1
            await state.update_data(current_bed=current_bed)
            await state.set_state(UserState.bedroom_area)
            await state.update_data(last_question=f'Расскажите какая площадь вашей {current_bed} спальни\n\nПример 1: 20,2\nПример 2: 12\nПример 3: Не знаю площадь\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await message.answer(f'Расскажите какая площадь вашей {current_bed} спальни\n\nПример 1: 20,2\nПример 2: 12\nПример 3: Не знаю площадь\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        else:
            await message.answer('Спасибо, что ответили на вопросы о спальнях, теперь продолжим разговор о квартире ❤️', reply_markup=await kb.Custom_Keyboard().agree_keyboard_back_to_flat())
            await state.update_data(last_question='Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинускую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().agree_keyboard_back_to_flat())
            
    # Обработчик начала ввода новой информации о квартире
    @staticmethod
    @router.callback_query(F.data=='okay')
    async def handle_info_about_beds(callback: CallbackQuery, state: FSMContext):
        await state.set_state(UserState.flat_view)
        await state.update_data(last_question='Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинускую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await callback.message.answer('Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинускую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
    
    # Ловим информацию о виде из окон квартиры
    @staticmethod
    @router.message(UserState.flat_view)
    async def handle_view_from_flat(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(flat_view=f"Виды из окон квартиры: {message.text}")
        await state.set_state(UserState.flat_area)
        await state.update_data(last_question='Укажите общую площадь квартиры\n\nПример 1 - 57,2\nПример 2 - 68\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await message.answer('Укажите общую площадь квартиры\n\nПример 1 - 57,2\nПример 2 - 68\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
    
    # Ловим информацию об общей площади квартиры
    @staticmethod
    @router.message(UserState.flat_area)
    async def handle_flat_area(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(flat_area=f"Общая площадь квартиры: {message.text}")
        await state.set_state(UserState.price)
        await state.update_data(last_question='Выберите валюту, в которой хотите указать цену\n')
        await state.update_data(last_keyboard=await kb.Custom_Keyboard().type_of_price())
        await message.answer('Выберите валюту, в которой хотите указать цену\n', reply_markup=await kb.Custom_Keyboard().type_of_price())
    
    # Ловим валюту цены и записываем в FSM
    @staticmethod
    @router.callback_query(UserState.price, F.data.in_(['rub', 'usd', 'rub/usd', 'money_back']))
    async def handle_number_of_value_price(callback: CallbackQuery, state: FSMContext):
        text_for_price = 'Пожалуйста введите цену в следующем формате\n\n'
        
        value_map = {
            'rub': f'{text_for_price}Пример 1 - 120 000 000\nПример 2 - 258 900 000\nПример 3 - Договорная',
            'usd': f'{text_for_price}Пример 1 - 120 000\nПример 2 - 258 900\nПример 3 - Договорная',
            'rub/usd': f'{text_for_price}Пример 1 - 12 000 000/13 6426.42\nПример 2 - 25 890 000/29 4340.01\nПример 3 - Договорная'
        }
        
        if callback.data in value_map:
            await state.update_data(price=f'Валюта квартиры: {callback.data}')
            await state.set_state(UserState.price_int)
            await state.update_data(last_question=f'{value_map[callback.data]}')
            await state.update_data(last_keyboard=None)
            await callback.message.answer(f'{value_map[callback.data]}')

        elif callback.data == "money_back":
            await state.set_state(UserState.flat_area)
            await state.update_data(last_question='Укажите общую площадь квартиры\n\nПример 1 - 57,2\nПример 2 - 68\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await callback.message.answer('Укажите общую площадь квартиры\n\nПример 1 - 57,2\nПример 2 - 68\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
    
    # Ловим цену квартиры цифрами
    @staticmethod
    @router.message(UserState.price_int)
    async def handle_flat_price(message: Message, state: FSMContext):
        price_text = message.text.replace(' ', '')
        if not price_text.isdigit():
            await message.answer("Пожалуйста, введите корректную сумму в формате 155 000 00.")
            return
        
        price_int = int(price_text)
        await state.update_data(price_int=f"Цена квартиры: {price_int:,}".replace(',', ' '))  # сохраняем сумму с пробелами
        
        await state.set_state(UserState.flat_details)
        await state.update_data(last_question='Расскажите кратко о достоинствах и плюсах квартиры\n\nПример 1 - До центра 10 минут, три парка рядом, в доме 4 ресторана\nПример 2 - В стоимость входит 2 м\м, Видно москву сити, до метро 2 минуты, консьерж\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ !!')
        await state.update_data(last_keyboard=None)
        await message.answer('Расскажите кратко о достоинствах и плюсах квартиры\n\nПример 1 - До центра 10 минут, три парка рядом, в доме 4 ресторана\nПример 2 - В стоимость входит 2 м\м, Видно москву сити, до метро 2 минуты, консьерж\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ !!')

    # Ловим детали о квартире
    @staticmethod
    @router.message(UserState.flat_details)
    async def handle_flat_details(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(flat_details=f"Достоинства и плюсы квартиры: {message.text}")
        await state.set_state(UserState.link_house)
        await state.update_data(last_question='Вставьте пожалуйста ссылку с ЦИАН с информацией о ЖК, в котором находится квартира')
        await state.update_data(last_keyboard=None)
        await message.answer('Вставьте пожалуйста ссылку с ЦИАН с информацией о ЖК, в котором находится квартира')
    
    # Ловим ссылки с Циана с ЖК
    @staticmethod
    @router.message(UserState.link_house)
    async def handle_link_of_house(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        url_pattern = r'^https:\/\/[\w-]+\.cian\.ru\/$'
        if re.match(url_pattern, message.text):
            await state.update_data(link_house=message.text)
            await state.set_state(UserState.jk_info_yes_or_no)  # просто чтобы статус проверить
            await state.update_data(last_question='Я беру информацию о вашем ЖК/доме с сайта ЦИАН. Не могли бы вы уточнить есть ли информация на ЦИАН о вашем прикрепленном ЖК/доме?')
            await state.update_data(last_keyboard=await kb.Custom_Keyboard().find_out_info_about_jk())
            await message.answer('Я беру информацию о вашем ЖК/доме с сайта ЦИАН. Не могли бы вы уточнить есть ли информация на ЦИАН о вашем прикрепленном ЖК/доме?', reply_markup=await kb.Custom_Keyboard().find_out_info_about_jk())
        else:
            await message.answer('Пожалуйста, введите корректную ссылку формата https://zhk-skyview-i.cian.ru/')

    # Ловим информацию о наличии текста на сайте ЦИАН
    @staticmethod
    @router.callback_query(UserState.jk_info_yes_or_no, F.data.in_(['yes_jk', 'no_jk', 'jk_back']))
    async def handle_info_about_jk(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'yes_jk':
            await state.set_state(UserState.jk_extra_info)
            await state.update_data(last_question='Здесь вы можете ввести информацию, которую ОБЯЗАТЕЛЬНО хотели бы учесть при формировании описания ЖК/дома\n\nПример 1 - дом построен в 1957 году, в нем жил знаменитый актер\nПример 2 - нет такой\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await callback.message.answer('Здесь вы можете ввести информацию, которую ОБЯЗАТЕЛЬНО хотели бы учесть при формировании описания ЖК/дома\n\nПример 1 - дом построен в 1957 году, в нем жил знаменитый актер\nПример 2 - нет такой\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!') 
            
        elif callback.data == 'no_jk':
            await state.update_data(link_house='')  # Очистите информацию о ссылке на ЖК
            await state.set_state(UserState.jk_written_info)
            await state.update_data(last_question='Пожалуйста вручную введите немного информации о ЖК/доме\n\nПример 1 - дом расположен недалеко от парка Горького, метро рядом, 7 этажей\nПример 2 - я не знаю/нет информации\nПример 3 - высококлассный жк с видом на Москву реку, внутри есть теннисный корт и футбольное поле, застройщик Sminex\nПример 4 - не знаю деталей\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
            await state.update_data(last_keyboard=None)
            await callback.message.answer('Пожалуйста вручную введите немного информации о ЖК/доме\n\nПример 1 - дом расположен недалеко от парка Горького, метро рядом, 7 этажей\nПример 2 - я не знаю/нет информации\nПример 3 - высококлассный жк с видом на Москву реку, внутри есть теннисный корт и футбольное поле, застройщик Sminex\nПример 4 - не знаю деталей\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        elif callback.data == 'jk_back':
            await state.set_state(UserState.link_house)
            await state.update_data(last_question='Вставьте пожалуйста ссылку с ЦИАН с информацией о ЖК, в котором находится квартира')
            await state.update_data(last_keyboard=None)
            await callback.message.answer('Вставьте пожалуйста ссылку с ЦИАН с информацией о ЖК, в котором находится квартира')

    # Ловим информацию о жк\доме, введенную вручную
    @staticmethod
    @router.message(UserState.jk_written_info)
    async def handle_written_jk(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(jk_written_info = f'Информация о жк: {message.text}')
        await state.set_state(UserState.jk_extra_info)
        await state.update_data(last_question='Здесь вы можете ввести информацию, которую ОБЯЗАТЕЛЬНО хотели бы учесть при формировании описания ЖК/дома\n\nПример 1 - дом построен в 1957 году, в нем жил знаменитый актер\nПример 2 - нет такой\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await message.answer('Здесь вы можете ввести информацию, которую ОБЯЗАТЕЛЬНО хотели бы учесть при формировании описания ЖК/дома\n\nПример 1 - дом построен в 1957 году, в нем жил знаменитый актер\nПример 2 - нет такой\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!') 

    # Ловим ОБЯЗАТЕЛЬНУЮ информацию о жк
    @staticmethod
    @router.message(UserState.jk_extra_info)
    async def handle_extra_info_about_jk(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(jk_extra_info = f"ОБЯЗАТЕЛЬНО учесть следующую информацию о ЖК: {message.text}")
        
        # Объединяем данные и создаем асинхронную задачу для уникализации текста
        data = await state.get_data()
        link_house = data.get('link_house', '')
        jk_written_info = data.get('jk_written_info', '')
        jk_extra_info = data.get('jk_extra_info', '')

        # Определяем, какую информацию использовать для описания ЖК
        if link_house:
            info = link_house
        else:
            info = jk_written_info

        asyncio.create_task(DescriptionConstructorHandler.uniquely_describe_building(info, jk_extra_info, state))
        
        await state.set_state(UserState.info_about_extra_rooms)
        await state.update_data(last_question='Если в вашей квартире есть дополнительные комнаты, то перечислите их\n\nПример 1 - нет таких/нет\nПример 2 - есть постирочная, гардеробная, балкон\nПример 3 - лоджия, гардеробная\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await message.answer('Если в вашей квартире есть дополнительные комнаты, то перечислите их\n\nПример 1 - нет таких/нет\nПример 2 - есть постирочная, гардеробная, балкон\nПример 3 - лоджия, гардеробная\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')

    # Ловим информацию о дополнительных комнатах
    @staticmethod
    @router.message(UserState.info_about_extra_rooms)
    async def handle_info_about_extra_rooms(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(info_about_extra_rooms = f"В квартире дополнительные комнаты: {message.text}")
        await state.set_state(UserState.flat_extra_info)
        await state.update_data(last_question="Пожалуйста укажите информацию, которую мне стоит ОБЯЗАТЕЛЬНО учесть и включить в описание квартиры\n\nПример 1 - в квартире проживал знаменитый актер, в квартире разрешен снос межкомнатных стен\nПример 2 - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!")
        await state.update_data(last_keyboard=None)
        await message.answer("Пожалуйста укажите информацию, которую мне стоит ОБЯЗАТЕЛЬНО учесть и включить в описание квартиры\n\nПример 1 - в квартире проживал знаменитый актер, в квартире разрешен снос межкомнатных стен\nПример 2 - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!")
    
    # Ловим дополнительную информацию для ОБЯЗАТЕЛЬНОГО добавления в описание
    @staticmethod
    @router.message(UserState.flat_extra_info)
    async def handle_extra_info_about_flat(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return
        
        await state.update_data(flat_extra_info = f'При формировании описания квартиры ОБЯЗАТЕЛЬНО учесть {message.text}')
        await state.set_state(UserState.deal_term) # просто переключиться для проверки статуса
        await state.update_data(last_question='Расскажите об условиях сделки. УКАЗАТЬ ОБЯЗАТЕЛЬНО\n\nПример 1 - 1 взрослый собственник, прямая продажа\nПример 2 - Торг, готовы выслушать ваше предложение по цене, Дизайн проект в подарок\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
        await state.update_data(last_keyboard=None)
        await message.answer('Расскажите об условиях сделки. УКАЗАТЬ ОБЯЗАТЕЛЬНО\n\nПример 1 - 1 взрослый собственник, прямая продажа\nПример 2 - Торг, готовы выслушать ваше предложение по цене, Дизайн проект в подарок\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!')
    
    @router.message(UserState.deal_term)
    async def handle_deal_term(message: Message, state: FSMContext):
        if message.text.startswith('/'):
            await DescriptionConstructorHandler.check_status(message, state)
            return

        await state.update_data(deal_term=f'Условия сделки - {message.text}')

        # Перед генерацией описания квартиры ждем создания описания ЖК
        data = await state.get_data()
        unique_description_of_building = data.get('unique_description_of_building', '')
        
        # Если описание ЖК еще не готово, подождем его
        if not unique_description_of_building:
            await message.answer('Пожалуйста подождите, идет генерация описания ЖК...')
            while not unique_description_of_building:
                await asyncio.sleep(1)  # Ожидание 1 секунду перед повторной проверкой
                data = await state.get_data()
                unique_description_of_building = data.get('unique_description_of_building', '')
        
        flat_info, jk_info = await DescriptionConstructorHandler.collect_info_from_fsm(state)  # собираем всю инфу из user state

        await message.answer('Генерирую ваше описание! Пожалуйста подождите. Займет не более 30 секунд!')
        await DescriptionConstructorHandler.create_unique_description_of_flat(flat_info, jk_info, state)
        await state.set_state(UserState.description_ready)
        await DescriptionConstructorHandler.send_description_to_user(message, state)

    @staticmethod
    @router.message(UserState.description_ready)
    async def send_description_to_user(message: Message, state: FSMContext):
        data = await state.get_data()
        flat_text = data.get('flat_text', 'Описание не найдено')
        await message.answer(f"Описание вашей квартиры:\n\n{flat_text}", reply_markup=await kb.Custom_Keyboard().stay_reload_function())

    # Ловим для переделки описания
    @staticmethod
    @router.callback_query(F.data == 'reload')
    async def reload_post(callback: CallbackQuery, state: FSMContext):
        await callback.message.answer('Переделываю описание...Займет не более 30 секунд')  # Отвечаем на callback сразу
        flat_info, jk_info = await DescriptionConstructorHandler.collect_info_from_fsm(state)  # собираем всю инфу из user state
        flat_text = await create_description_of_flat(flat_info, jk_info)
        await state.update_data(flat_text=flat_text)
        await callback.message.answer(flat_text, reply_markup=await kb.Custom_Keyboard().stay_reload_function())

    # Ловим для отправки поста без переделывания
    @staticmethod
    @router.callback_query(F.data == 'stay')
    async def send_post_cian(callback: CallbackQuery, state: FSMContext):
        await callback.message.answer('Направляю вам постик...')  # Отвечаем на callback сразу
        data = await state.get_data()  # получаем сохраненное состояние файла чтобы отправить неизменнеый текст
        await callback.message.answer(data['flat_text'])
        await callback.message.answer('Рад был вам помочь ❤️\n\nДавайте сформируем еще одно красивое описание с вами! Вам так же нужно будет рассказать мне всё о вашей квартире!', reply_markup=await kb.Custom_Keyboard().agree_keyboard())
        await state.clear()

    # функция для проверки текущего состояния пользователя и вывод ранее введенной информации
    @staticmethod
    @router.message(Command('status'))
    async def check_status(message: Message, state: FSMContext):
        data = await state.get_data()
        responses = []
        responses.append(f"Количество комнат в квартире: {data.get('number_of_rooms', 'не указано')}\n")
        responses.append(f"Состояние ремонта: {data.get('renovation_status', 'не указано')}\n")
        responses.append(f"Стиль квартиры: {data.get('style', 'не указано')}\n")
        responses.append(f"Кухня совмещена с гостиной: {data.get('kitchen_living_room', 'не указано')}\n")
        responses.append(f"Количество санузлов: {data.get('number_of_closet', 'не указано')}\n")
        responses.append(f"Количество спален: {data.get('number_of_bedrooms', 'не указано')}\n")

        if data.get('number_of_bedrooms', 0) > 0:
            bed_count = int(data.get('number_of_bedrooms', 0))
            bedrooms_info = [
                f"Спальня {i + 1}: Площадь - {data.get(f'bedroom_{i+1}_area', 'не указано')}, Санузел - {data.get(f'bedroom_{i+1}_wc', 'не указано')}, Тип - {data.get(f'bedroom_{i+1}_type', 'не указано')}, Вид - {data.get(f'bedroom_{i+1}_view', 'не указано')}, Вид из окон спален - {data.get(f'bedroom_{i+1}_details', 'не указано')}"
                for i in range(bed_count)
            ]
            responses.append("Информация о спальнях:\n" + "\n".join(bedrooms_info))
        else:
            responses.append("Информация о спальнях не указана.")

        responses.append(f"Виды из окон квартиры: {data.get('flat_view', 'не указано')}\n")
        responses.append(f"Общая площадь квартиры: {data.get('flat_area', 'не указано')}\n")
        responses.append(f"Валюта цены: {data.get('price', 'не указано')}\n")
        responses.append(f"Цена квартиры: {data.get('price_int', 'не указано')}\n")
        responses.append(f"Достоинства и плюсы квартиры: {data.get('flat_details', 'не указано')}\n")
        responses.append(f"Ссылка на информацию о ЖК: {data.get('link_house', 'не указано')}\n")
        responses.append(f"Дополнительная информация о ЖК: {data.get('jk_written_info', 'не указано')}\n")
        responses.append(f"ВАЖНЫЕ замечания о ЖК: {data.get('jk_extra_info', 'не указано')}\n")
        responses.append(f"Дополнительные комнаты в квартире: {data.get('info_about_extra_rooms', 'не указано')}\n")
        responses.append(f"ВАЖНАЯ информация о квартире: {data.get('flat_extra_info', 'не указано')}\n")
        responses.append(f"Описание жк после gpt: {data.get('unique_description_of_building', 'не указано')}\n")
        responses.append(f"Условия сделки: {data.get('deal_term', 'не указано')}\n")

        await message.answer("\n".join(responses))

        # Возвращаем пользователя к предыдущему состоянию, вопросу и клавиатуре
        last_question = data.get('last_question', None)
        last_keyboard = data.get('last_keyboard', None)
        
        if last_question:
            if last_keyboard:
                await message.answer(last_question, reply_markup=last_keyboard)
            else:
                await message.answer(last_question)
        
        current_state = await state.get_state()
        await state.set_state(current_state)

    @staticmethod
    @router.message(Command('help'))
    async def show_help(message: Message):
        await message.answer('/start - позволяет запустить и перезаустить бота\n/status - выводит текущую инфомацию о квартире в конструкторе описания\n\n\
        КНОПКА Конструктор Описания квартиры - инструмент, который позволит вам создать идеальное описание квартиры по введенным параметрам')