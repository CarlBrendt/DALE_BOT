from aiogram import F, Router
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, CallbackQuery
import subprocess

import aiohttp
from app.states import Status as State_Status
import keyboard.status_keyboard as st_kb
from PIL import Image
import os

from playwright.async_api import async_playwright

router = Router()

subprocess.run(["playwright", "install"])

class Status:
    
    __template_map = {
        'first_template': 'Первый шаблон',
        'second_template': 'Второй шаблон',
        'third_template': 'Третий шаблон',
        'fourth_template': 'Четвертый шаблон',
        'fifth_template': 'Пятый шаблон',
        'six_template': 'Шестой шаблон'
    }
    
    '''
    __file_path = [
        r".\app\status\status_templates\первый_шаблон.png",
        r".\app\status\status_templates\второй_шаблон.png",
        r".\app\status\status_templates\третий_шаблон.png",
        r".\app\status\status_templates\четвертый_шаблон.png",
        r".\app\status\status_templates\пятый_шаблон.png",
        r".\app\status\status_templates\шестой_шаблон.png"
    ]
    '''
    # для докера
    __file_path = [
        r"./app/status/status_templates/первый_шаблон.png",
        r"./app/status/status_templates/второй_шаблон.png",
        r"./app/status/status_templates/третий_шаблон.png",
        r"./app/status/status_templates/четвертый_шаблон.png",
        r"./app/status/status_templates/пятый_шаблон.png",
        r"./app/status/status_templates/шестой_шаблон.png"
    ]

    compressed_path = r".\app\status\compressed_templates"
    photo_cache = []  
    
    @staticmethod
    def compress_image(input_path, output_path, quality=70):
        """Функция сжатия изображений."""
        with Image.open(input_path) as img:
            img.save(output_path, "JPEG", quality=quality)

    @staticmethod
    @router.message(F.text.in_(["📱 Сформировать статус"]))
    async def handle_status(message: Message, state: FSMContext):
        await state.clear()
        if not Status.photo_cache:
            await message.answer('Пожалуйста выберите один из понравившихся шаблонов для дальнейшего формирования вашего статуса')

            # Создаем папку для сжатых изображений, если она не существует
            if not os.path.exists(Status.compressed_path):
                os.makedirs(Status.compressed_path)

            compressed_photos = []
            for photo in Status.__file_path:
                compressed_photo = os.path.join(Status.compressed_path, os.path.basename(photo))
                Status.compress_image(photo, compressed_photo)
                compressed_photos.append(FSInputFile(compressed_photo))

            # Отправляем медиа-группу и сохраняем file_id
            media_group = [
                InputMediaPhoto(media=compressed_photos[0], caption='Первый шаблон'),
                InputMediaPhoto(media=compressed_photos[1], caption="Второй шаблон"),
                InputMediaPhoto(media=compressed_photos[2], caption='Третий шаблон'),
                InputMediaPhoto(media=compressed_photos[3], caption="Четвертый шаблон"),
                InputMediaPhoto(media=compressed_photos[4], caption='Пятый шаблон'),
                InputMediaPhoto(media=compressed_photos[5], caption="Шестой шаблон")
            ]
            messages = await message.answer_media_group(media_group)

            # Сохраняем file_id после первой отправки
            Status.photo_cache = [msg.photo[-1].file_id for msg in messages]

        else:
            await message.answer('Пожалуйста выберите один из понравившихся шаблонов для дальнейшего формирования вашего статуса')

            # Если file_id уже сохранены, повторно отправляем медиа-группу с использованием file_id
            media_group = [
                InputMediaPhoto(media=file_id, caption=f'Шаблон {index + 1}')
                for index, file_id in enumerate(Status.photo_cache)
            ]
            await message.answer_media_group(media_group)

        await state.set_state(State_Status.choosing_template)
        await message.answer("Выберите понравившийся вам шаблон статуса", reply_markup=await st_kb.Custom_Status_Keyboard().choose_template_first())

    @staticmethod
    @router.callback_query(State_Status.choosing_template, F.data.in_([
        "first_template", "second_template", "third_template", 
        "fourth_template", "fifth_template", "six_template",     
        "forward_template", "back_template"
    ]))
    async def handle_template_choosing(callback: CallbackQuery, state: FSMContext):
        
        if callback.data in Status.__template_map.keys():
            
            selected_template = Status.__template_map[callback.data]
            await state.update_data(choosing_template=selected_template)
            
            await state.set_state(State_Status.first_three_components)
            await callback.message.answer(f'Вы выбрали: {selected_template}. Пожалуйста ответьте на несколько вопросов, чтобы я мог составить правильный статус для вас!')
            await callback.message.answer('Заполните поле 1, если его нет, напишите НЕТ\n\nP.S. Напишите мне то, что вы бы хотели увидеть в этом поле, как на рисунке')
            
        elif callback.data == 'forward_template':
            await callback.message.edit_text(
                "Выберите понравившийся вам шаблон статуса", 
                reply_markup=await st_kb.Custom_Status_Keyboard().choose_template_second()
            )

        elif callback.data == 'back_template':
            await callback.message.edit_text(
                "Выберите понравившийся вам шаблон статуса", 
                reply_markup=await st_kb.Custom_Status_Keyboard().choose_template_first()
            )
            
    # ловим первые три компонента для создания шаблона   
    # если это второй шабблон, то там будет 4 компонента
    
    @staticmethod
    @router.message(State_Status.first_three_components)
    async def handle_first_three_components(message: Message, state: FSMContext):
        
        # Получаем текущие данные состояния
        data = await state.get_data()
        
        # Проверяем, какие данные уже были введены
        if '1 строка' not in data:
            await state.update_data({'1 строка': message.text})
            await message.answer('Заполните поле 2, если его нет, напишите НЕТ\n\nP.S. Напишите мне то, что вы бы хотели увидеть в этом поле, как на рисунке')
        
        elif '2 строка' not in data:
            await state.update_data({'2 строка': message.text})
            await message.answer('Заполните поле 3, если его нет, напишите НЕТ\n\nP.S. Напишите мне то, что вы бы хотели увидеть в этом поле, как на рисунке')
        
        elif '3 строка' not in data:
            await state.update_data({'3 строка': message.text})
            
            if data['choosing_template'] == 'Второй шаблон':
                await message.answer('Заполните поле 4, если его нет, напишите НЕТ\n\nP.S. Напишите мне то, что вы бы хотели увидеть в этом поле, как на рисунке')
                await state.set_state(State_Status.fourth_component)
            else:
                # Все три строки введены, переходим к следующему состоянию
                await state.set_state(State_Status.common_components)
                await message.answer('📐 Введите площадь вашей квартиры')
    
    # 4 поле для статуса со второго шаблона        
    @staticmethod
    @router.message(State_Status.fourth_component)
    async def handle_fourth_component(message: Message, state: FSMContext):
        await state.update_data({'4 строка': message.text})
        # Переходим к следующему состоянию
        await state.set_state(State_Status.common_components)
        await message.answer('📐 Введите площадь вашей квартиры')
    
    @staticmethod
    @router.message(State_Status.common_components)
    async def handle_common_components(message: Message, state: FSMContext):
        data = await state.get_data()

        # Определяем список вопросов и ключи для данных
        if data['choosing_template'] == 'Второй шаблон':
            questions = [
                ('площадь', '🛌 Введите количество спален'),
                ('спальни', '🏬 Введите этаж'),
                ('этаж', '🪜 Введите высоту потолка'),
                ('потолок', '💰 Укажите цену квартиры в формате 120 000 000'),
                ('цена', '🎁 Укажите цену со скидкой в формате 120 000 000, если она УКАЗАНА в шаблоне, если нет напишите НЕТ'), 
                ('скидочная_цена', 'Пришлите фото'), 
            ]
            next_state = State_Status.photo
        else:
            questions = [
                ('площадь', '🛌 Введите количество спален'),
                ('спальни', '🚻 Введите количество санузлов'),
                ('санузлы', '🏬 Введите этаж'),
                ('этаж', '💰 Укажите цену квартиры в формате 120 000 000'),
                ('цена', '🎁 Укажите цену со скидкой в формате 120 000 000, если она УКАЗАНА в шаблоне, если нет напишите НЕТ'), 
                ('скидочная_цена', 'Пришлите фото'), 
            ]
            next_state = State_Status.photo

        # Итерируемся по вопросам и обновляем данные
        for key, question in questions:
            if key not in data:
                if key == 'цена' or key == 'скидочная_цена':
                    # Validate price input
                    price_text = message.text.replace(' ', '')  # Remove spaces
                    if not price_text.isdigit() and key == 'цена':
                        await message.answer("Пожалуйста, введите корректную сумму в формате 120000000.")
                        return  # Wait for the next response
                    
                    if key == 'цена':
                    # If valid, update state with price
                        await state.update_data({key: int(price_text)})
                    elif key == 'скидочная_цена':
                        await state.update_data({key: price_text})    
                else:
                    await state.update_data({key: message.text})
                
                await message.answer(question)
                
                if question == 'Пришлите фото':
                    if data['choosing_template'] == 'Пятый шаблон':
                        await message.answer('Пожалуйста, загрузите 2 фото ПООЧЕРЕДНО в том же порядке, что и на шаблоне.\nСначала загрузите ОДНО фото, дождитесь оповещения и загружайте следующее')
                    else:
                        await message.answer('Пожалуйста, загрузите 4 фото ПООЧЕРЕДНО в том же порядке, что и на шаблоне.\nСначала загрузите ОДНО фото, дождитесь оповещения и загружайте следующее')
                    
                    await state.set_state(next_state)
                    
                return  # Ожидаем следующий ответ
                
    @router.message(State_Status.photo, F.photo)
    async def handle_template_photo_from_user(message: Message, state: FSMContext):
        
        data = await state.get_data()
        
        # Получаем список уже сохраненных фото
        photos = data.get('photos', [])
        
        # Скачиваем фотографию с самым высоким разрешением
        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        file_path = file_info.file_path
        
        # Создаем уникальное имя файла
        photo_number = len(photos) + 1
        save_path = f'.\\status\\to_server\\photo_{photo_number}_{message.from_user.id}.jpg'
        
        # Сохраняем фотографию
        await message.bot.download_file(file_path, save_path)
        photos.append(save_path)

        # Отправляем фотографию на FastAPI серв # Ваш FastAPI сервер
    
        data_for_server = {
            'photo_number': str(photo_number),
            'user_id': str(message.from_user.id)
        }
        # Открываем файл для передачи
        with open(save_path, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('photo_number', str(photo_number))
            form_data.add_field('user_id', str(message.from_user.id))
            form_data.add_field('file', file, filename=f'photo_{photo_number}.jpg', content_type='image/jpeg')

            url = 'https://deil-server-2c040b241127.herokuapp.com/generation/upload_photo'

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=form_data) as response:
                    if response.status == 200:
                        print("Данные успешно добавлены:", await response.json())
                    else:
                        print("Ошибка при добавлении данных:", response.status, await response.text())
                        
        # Обновляем данные состояния
        await state.update_data(photos=photos)
        
        if data['choosing_template'] == 'Пятый шаблон':
            if len(photos) < 2:
                await message.answer(f"Фото {photo_number} успешно сохранено! Пожалуйста, отправьте следующее фото.")
            else:
                await message.answer("Все 2 фото успешно сохранены!")
                await state.set_state(State_Status.create_template)
                await message.answer("Нажмите, чтобы получить статус, и подождите пару секунд ⌛️", reply_markup=await st_kb.Custom_Status_Keyboard().get_template())
        
        else:  # Для остальных шаблонов
            if len(photos) < 4:
                await message.answer(f"Фото {photo_number} успешно сохранено! Пожалуйста, отправьте следующее фото.")
            else:
                await message.answer("Все 4 фото успешно сохранены!")
                await state.set_state(State_Status.create_template)
                await message.answer("Нажмите, чтобы получить статус, и подождите пару секунд ⌛️", reply_markup=await st_kb.Custom_Status_Keyboard().get_template())
    @staticmethod
    async def post_request_to_api(data_dict, api_url, telegram_id, session: aiohttp.ClientSession) -> None:
        print(data_dict)
        
        # Данные для отправки
        data_for_server = {
            "user_id": telegram_id,
            "first_area": data_dict['1 строка'],
            "second_area": data_dict['2 строка'],
            "third_area": data_dict['3 строка'],
            "area": data_dict['площадь'],
            "bedroom": data_dict['спальни'],
            "floor": data_dict['этаж'],
            "price": data_dict['цена'],
            "sales_price": data_dict['скидочная_цена'],
            "path": data_dict['photos']
        }
        
        if 'all' in api_url:
            data_for_server['restroom'] = int(data_dict['санузлы'])
            
        else:
            
            data_for_server["fourth_area"] = data_dict['4 строка']
            
            data_for_server["ceiling"] = int(data_dict['потолок'])
        
        # POST-запрос для добавления данных
        async with session.post(api_url, json=data_for_server) as response:
            if response.status == 200:
                print("Данные успешно добавлены:", await response.json())
            else:
                print("Ошибка при добавлении данных:", response.status, await response.text())
    
    @staticmethod
    async def take_screenshot(url: str, user_id):
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Open the target website
            await page.goto(url)

            # Take a screenshot of the web page
            await page.screenshot(path=f".\\status\\template_screenshots\\screenshot_{user_id}.png", full_page=True)

            # Close the browser instance
            await browser.close()
    
    @staticmethod
    async def save_image_from_url_template(user_id, state: FSMContext):
        
        data = await state.get_data()
        
        common_endpoint = 'https://deil-server-2c040b241127.herokuapp.com/pages/'
        
        if data['choosing_template'] == 'Третий шаблон':
            
            image_url = f'{common_endpoint}third_template?user_id={user_id}&template=first'
            
        elif data['choosing_template'] == 'Второй шаблон':
            
            image_url = f'{common_endpoint}second_template?user_id={user_id}&template=second'
        
        elif data['choosing_template'] == 'Четвертый шаблон':
            
            image_url = f'{common_endpoint}fourth_template?user_id={user_id}&template=first'
        
        elif data['choosing_template'] == 'Первый шаблон':
            
            image_url = f'{common_endpoint}first_template?user_id={user_id}&template=first'
        
        elif data['choosing_template'] == 'Пятый шаблон':
            
            image_url = f'{common_endpoint}fifth_template?user_id={user_id}&template=first'
        
        elif data['choosing_template'] == 'Шестой шаблон':
            
            image_url = f'{common_endpoint}six_template?user_id={user_id}&template=first'
        
        try:
            await Status.take_screenshot(image_url, user_id=user_id)
        
            print({"status": "success", "message": "Image generated successfully."})
        except Exception as e:
            print(e)
            
    # Метод для отправки данных в баху данных через Aiogram
    @staticmethod
    @router.callback_query(State_Status.create_template, F.data == 'get_template')
    async def handle_post_request(call: CallbackQuery, state: FSMContext) -> None:
        
        data = await state.get_data()
        
        print(data['choosing_template'])
        
        # Определяем URL
        if data['choosing_template'] == 'Второй шаблон':
            
            api_url = "https://deil-server-2c040b241127.herokuapp.com/generation/api/add_data"
        else:
            api_url = "https://deil-server-2c040b241127.herokuapp.com/generation/api/add_data/all"

        async with aiohttp.ClientSession() as session:
            # Используем одну и ту же сессию для всех операций
            await Status.post_request_to_api(data_dict=data, api_url=api_url, telegram_id=call.from_user.id, session=session)

            await Status.save_image_from_url_template(user_id=call.from_user.id, state=state)
        
        user_id = call.from_user.id
        
        output_image_path = f".\\status\\template_screenshots\\screenshot_{user_id}.png"
        
        await call.message.answer_photo(
                    FSInputFile(path=output_image_path), caption="Ваш статус ❤️"
        )
        
        await state.clear()
        
        if not Status.photo_cache:
            await call.message.answer('Пожалуйста выберите один из понравившихся шаблонов для дальнейшего формирования вашего статуса. Немного подождите')

            # Создаем папку для сжатых изображений, если она не существует
            if not os.path.exists(Status.compressed_path):
                os.makedirs(Status.compressed_path)

            compressed_photos = []
            for photo in Status.__file_path:
                compressed_photo = os.path.join(Status.compressed_path, os.path.basename(photo))
                Status.compress_image(photo, compressed_photo)
                compressed_photos.append(FSInputFile(compressed_photo))

            # Отправляем медиа-группу и сохраняем file_id
            media_group = [
                InputMediaPhoto(media=compressed_photos[0], caption='Первый шаблон'),
                InputMediaPhoto(media=compressed_photos[1], caption="Второй шаблон"),
                InputMediaPhoto(media=compressed_photos[2], caption='Третий шаблон'),
                InputMediaPhoto(media=compressed_photos[3], caption="Четвертый шаблон"),
                InputMediaPhoto(media=compressed_photos[4], caption='Пятый шаблон'),
                InputMediaPhoto(media=compressed_photos[5], caption="Шестой шаблон")
            ]
            messages = await call.message.answer_media_group(media_group)

            # Сохраняем file_id после первой отправки
            Status.photo_cache = [msg.photo[-1].file_id for msg in messages]

        else:
            await call.message.answer('Пожалуйста выберите один из понравившихся шаблонов для дальнейшего формирования вашего статуса')

            # Если file_id уже сохранены, повторно отправляем медиа-группу с использованием file_id
            media_group = [
                InputMediaPhoto(media=file_id, caption=f'Шаблон {index + 1}')
                for index, file_id in enumerate(Status.photo_cache)
            ]
            await call.message.answer_media_group(media_group)

        await state.set_state(State_Status.choosing_template)
        await call.message.answer("Выберите понравившийся вам шаблон статуса", reply_markup=await st_kb.Custom_Status_Keyboard().choose_template_first())