import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class Custom_Keyboard:
    
    def __init__(self) -> None:
        # кнопки уровня доступа в зависимости от уровня доступа
        with open('database/access.json', encoding='UTF-8') as f:
            self._access_buttons = json.load(f)
            
        # ники пользователей с разными доступами
        with open('database/user_names_for_access.json', encoding='UTF-8') as f:
            self._user_names = json.load(f)
    
    async def main_keyboard(self, user_name: str) -> ReplyKeyboardMarkup:
        """
        Функция для построения кнопок в зависимости от уровня доступа
        """
        keyboard_reply_builder = ReplyKeyboardBuilder()
        keyboard_constructor = []


        if user_name in self._user_names['admin']:
            keyboard_constructor = self._access_buttons['admin']
        elif user_name in self._user_names['brokers']:
            keyboard_constructor = self._access_buttons['brokers']

        for button in keyboard_constructor:
            keyboard_reply_builder.add(KeyboardButton(text=button))

        return keyboard_reply_builder.adjust(2).as_markup(resize_keyboard=True)

    async def stay_reload_function(self) -> InlineKeyboardMarkup:
        
        # Клавиатура для того чтобы выбирать что делать с постом Циан
        stay_reload_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Оставить это описание', callback_data='stay')],
                [InlineKeyboardButton(text='Рерайт описания с теми же данными', callback_data='reload')]
            ]
        )
        return stay_reload_keyboard
    
    async def go_back_to_description_keyboard(self) -> InlineKeyboardMarkup:
        
        # Клавиатура для того чтобы выбрать режим описания 
        go_back = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='back')]
            ]
        )
        return go_back

    async def rooms_select_keyboard(self) -> InlineKeyboardMarkup:

        # Клавиатура для того чтобы выбрать количество комнат в квартире
        rooms_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='1 комната', callback_data='one_room')],
                [InlineKeyboardButton(text='2 комнаты', callback_data='two_rooms')],
                [InlineKeyboardButton(text='3 комнаты', callback_data='three_rooms')],
                [InlineKeyboardButton(text='4+ комнат', callback_data='many_rooms')],
                [InlineKeyboardButton(text='Студия', callback_data='studio')],
                [InlineKeyboardButton(text='Свободная планировка', callback_data='empty')],
                [InlineKeyboardButton(text='Назад', callback_data='rooms_backs')]
            ]
        )
        return rooms_keyboard
    
    # Клавиатура чтобы выбрать есть ли отделка в квартире
    async def select_renovation_keyboard(self) -> InlineKeyboardMarkup:
        renovation_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='С отделкой', callback_data='with_renovation')],
                [InlineKeyboardButton(text='Без отделки', callback_data='no_renovation')],
                [InlineKeyboardButton(text='Назад', callback_data='renovation_backs')]
            ]
        )
        return renovation_keyboard
    
    # Клавиатура чтобы проверить совмещена ли кухня с гостинной
    async def kitchen_with_living_room_keyboard(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Да', callback_data='yes_single_room')],
                [InlineKeyboardButton(text='Кухня и гостиная две разные комнаты', callback_data='no_single_room')],
                [InlineKeyboardButton(text='Назад', callback_data='single_room_back')]
            ]
        )
        return select_keyboard
    
    # Клавиатура чтобы выбрать количество санузлов во всей квартире
    async def wc_select_keyboard(self) -> InlineKeyboardMarkup:
        
        wc_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='1 санузел', callback_data='one_wc')],
                [InlineKeyboardButton(text='2 санузла', callback_data='two_wc')],
                [InlineKeyboardButton(text='3 санузла', callback_data='three_wc')],
                [InlineKeyboardButton(text='4+ санузла', callback_data='many_wc')],
                [InlineKeyboardButton(text='Назад', callback_data='wc_backs')]
            ]
        )
        return wc_keyboard

    async def agree_keyboard(self) -> InlineKeyboardMarkup:
        agree_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Хорошо', callback_data='I_agree')]])
        return agree_keyboard
    
    # Клавиатура чтобы выбрать количество спален во всей квартире
    async def bedroom_select_keyboard(self) -> InlineKeyboardMarkup:
        
        bed_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='1 спальня', callback_data='one_bed')],
                [InlineKeyboardButton(text='2 спальни', callback_data='two_bed')],
                [InlineKeyboardButton(text='3 спальни', callback_data='three_bed')],
                [InlineKeyboardButton(text='4+ спальни', callback_data='many_bed')],
                [InlineKeyboardButton(text='Назад', callback_data='bed_backs')]
            ]
        )
        return bed_keyboard
            
    # Проверка есть ли личный туалет в спальне
    async def number_of_wc_in_bedroom(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Да', callback_data='yes_wc_bed')],
                [InlineKeyboardButton(text='Нет', callback_data='no_wc_bed')],
                [InlineKeyboardButton(text='Назад', callback_data='wc_bed_back')]
            ]
        )
        return select_keyboard
    
    # Просто спрашиваем понятно ли что мы сейчас будем побирать информацию о каждой спальне
    async def agree_keyboard_about_bed(self) -> InlineKeyboardMarkup:
        agree_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Понятно', callback_data='got_it')]])
        return agree_keyboard
    
    # Выбираем тип каждой спальни
    async def type_of_bedroom(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Мастер', callback_data='master')],
                [InlineKeyboardButton(text='Гостевая', callback_data='guest')],
                [InlineKeyboardButton(text='Детская', callback_data='kids')],
                [InlineKeyboardButton(text='Назад', callback_data='type_back')]
            ]
        )
        return select_keyboard
    
    # Выбираем валюту
    async def type_of_price(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='RUB', callback_data='rub')],
                [InlineKeyboardButton(text='USD', callback_data='usd')],
                [InlineKeyboardButton(text='RUB/USD', callback_data='rub/usd')],
                [InlineKeyboardButton(text='Назад', callback_data='money_back')]
            ]
        )
        return select_keyboard
        
    # Просто спрашиваем понятно ли что мы сейчас возвращаемся к описанию квартиры
    async def agree_keyboard_back_to_flat(self) -> InlineKeyboardMarkup:
        agree_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Я поняла/понял', callback_data='okay')]])
        return agree_keyboard
    
    async def find_out_info_about_jk(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Да, на сайте Циан есть описание ЖК/дома', callback_data='yes_jk')],
                    [InlineKeyboardButton(text='Нет, на сайте Циан нет описания ЖК/дома', callback_data='no_jk')],
                    [InlineKeyboardButton(text='Назад', callback_data='jk_back')]
                ]
            )
        return select_keyboard
    
if __name__ == "__main__":
    kb = Custom_Keyboard()
    print(kb.main_keyboard)
