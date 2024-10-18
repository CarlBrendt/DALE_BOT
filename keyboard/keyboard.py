<<<<<<< HEAD
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

    # Клавиатура чтобы пополнить баланс или оставить
    async def upprove_balance(self) -> InlineKeyboardMarkup:
        balance_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='💰 Пополнить баланс', callback_data='yes_balance')],
                [InlineKeyboardButton(text='❌ Пополнить позже', callback_data='no_balance')],
            ]
        )
        return balance_keyboard
    
    # Клавиатура на количество пополнения баланса
    async def amount_of_top_up(self) -> InlineKeyboardMarkup:
        balance_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='💰 100 рублей', callback_data='100_rub')],
                [InlineKeyboardButton(text='💰 150 рублей', callback_data='150_rub')],
                [InlineKeyboardButton(text='💰 500 рублей', callback_data='500_rub')],
                [InlineKeyboardButton(text='❌ Пополнить позже', callback_data='later')]
            ]
        )
        return balance_keyboard
    
    
    async def balance_options(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Пополнить на 50 рублей", callback_data="top_up_50"))
        keyboard.add(InlineKeyboardButton("Пополнить на 100 рублей", callback_data="top_up_100"))
        return keyboard
    
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
            inline_keyboard=[[InlineKeyboardButton(text='Далее', callback_data='I_agree')]])
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
    
    # Клавиатура чтобы сгенерировать описание
    async def generate_description(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='💰 5 руб.', callback_data='generate_description')],
            ]
        )
        return keyboard
    
    async def stay_reload_function(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Rewrite с теми же данными - 💰 3 руб (первые 3 бесплатно)', callback_data='reload')],
                    [InlineKeyboardButton(text='Оставить так', callback_data='stay')],
                ]
            )
        return select_keyboard
    
    async def change_parametrs(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Да, я хотел бы изменить некоторые параметры', callback_data='yes_change')],
                    [InlineKeyboardButton(text='Нет, не хочу менять', callback_data='no_change')],
                ]
            )
        return select_keyboard
    
    async def change_parameters_keyboard(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Количество комнат', callback_data='change_rooms')],
                [InlineKeyboardButton(text='Отделка квартиры', callback_data='change_renovation')],
                [InlineKeyboardButton(text='Стиль/ремонт квартиры', callback_data='change_style')],
                [InlineKeyboardButton(text='Совместимость кухни и гостиной', callback_data='change_kitchen')],
                [InlineKeyboardButton(text='Количество санузлов в квартире', callback_data='change_closet')],
                [InlineKeyboardButton(text='Количество спален в квартире', callback_data='change_bedrooms')],
                [InlineKeyboardButton(text='Санузел в спальне', callback_data='change_bedroom_wc')],
                [InlineKeyboardButton(text='Тип спальни', callback_data='change_bedroom_type')],
                [InlineKeyboardButton(text='Вид из спальни', callback_data='change_bedroom_view')],
                [InlineKeyboardButton(text='Вид из квартиры', callback_data='change_flat_view')],
                [InlineKeyboardButton(text='Площадь квартиры', callback_data='change_flat_area')],
                [InlineKeyboardButton(text='Изменить цену (Валюта не меняется)', callback_data='change_price')],
                [InlineKeyboardButton(text='Изменить достоинства квартиры', callback_data='change_flat_details')],
                [InlineKeyboardButton(text='Дополнительные комнаты', callback_data='change_extra_rooms')],
                [InlineKeyboardButton(text='ЖК с Циан / Дом', callback_data='change_jk_info')],
                [InlineKeyboardButton(text='Обязательная информация о квартире', callback_data='change_flat_extra_info')],
                [InlineKeyboardButton(text='Условия сделки', callback_data='change_deal_term')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back')]
            ]
        )
        return select_keyboard

    async def change_parameters_keyboard_one(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Количество комнат', callback_data='change_rooms')],
                [InlineKeyboardButton(text='Отделка квартиры', callback_data='change_renovation')],
                [InlineKeyboardButton(text='Стиль/ремонт квартиры', callback_data='change_style')],
                [InlineKeyboardButton(text='Совместимость кухни и гостиной', callback_data='change_kitchen')],
                [InlineKeyboardButton(text='Далее', callback_data='next_one')],
                [InlineKeyboardButton(text='К генерации описания', callback_data='change_back')]
            ])
            
        return select_keyboard
    
    async def change_parameters_keyboard_two(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Ремонт в квартире', callback_data='change_info_renovation')],
                [InlineKeyboardButton(text='ИНформацияо кухне/гостиной', callback_data='change_info_kitchen_living_room')],
                [InlineKeyboardButton(text='Количество санузлов в квартире', callback_data='change_closet')],
                [InlineKeyboardButton(text='Количество спален в квартире', callback_data='change_bedrooms')],
                [InlineKeyboardButton(text='Далее', callback_data='next_two')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back_two')]
            ])
            
        return select_keyboard

    async def change_parameters_keyboard_three(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                
                [InlineKeyboardButton(text='Вид из квартиры', callback_data='change_flat_view')],
                [InlineKeyboardButton(text='Площадь квартиры', callback_data='change_flat_area')],
                [InlineKeyboardButton(text='Изменить цену (Валюта не меняется)', callback_data='change_price')],
                [InlineKeyboardButton(text='Изменить достоинства квартиры', callback_data='change_flat_details')],
                
                [InlineKeyboardButton(text='Далее', callback_data='next_three')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back_three')]
            ])
            
        return select_keyboard
    
    async def change_parameters_keyboard_four(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Дополнительные комнаты', callback_data='change_extra_rooms')],
                [InlineKeyboardButton(text='Обязательная информация о квартире', callback_data='change_flat_extra_info')],
                [InlineKeyboardButton(text='Обязательная информация о ЖК/доме', callback_data= 'change_jk_extra_info')],
                [InlineKeyboardButton(text='Условия сделки', callback_data='change_deal_term')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back_four')]
            ])
            
        return select_keyboard
    
    async def support_keyboard_chose(self) -> ReplyKeyboardMarkup:
        """
        Функция для построения кнопок в зависимости от уровня доступа
        """
        keyboard_reply_builder = ReplyKeyboardBuilder()
        keyboard_constructor = ['📨 Тех.поддержка / QA', '📚 Про нас / Вакансии', 'Вернуться к основным разделам']

        for button in keyboard_constructor:
            keyboard_reply_builder.add(KeyboardButton(text=button))

        return keyboard_reply_builder.adjust(2).as_markup(resize_keyboard=True)
    
    async def support_variant(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='📲 Q/A с Разработчиком', callback_data='developer_qa')],
                [InlineKeyboardButton(text='📲 Q/A c Руководителем', callback_data='seo_qa')],

            ])
            
        return select_keyboard
    
    async def support_options_developer(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='❓ Задать вопрос', callback_data='question')],
                [InlineKeyboardButton(text='💡 Поделиться идеей или улучшением', callback_data='idea')],
                [InlineKeyboardButton(text='Назад', callback_data='support_back')],
            ])
            
        return select_keyboard
    
    async def support_options_seo(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='❓ Задать вопрос', callback_data='question_seo')],
                [InlineKeyboardButton(text='💡 Поделиться идеей или улучшением', callback_data='idea_seo')],
                [InlineKeyboardButton(text='Назад', callback_data='support_back_seo')],
            ])
            
        return select_keyboard
    
    
if __name__ == "__main__":
    kb = Custom_Keyboard()
    print(kb.main_keyboard)
=======
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

    # Клавиатура чтобы пополнить баланс или оставить
    async def upprove_balance(self) -> InlineKeyboardMarkup:
        balance_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='💰 Пополнить баланс', callback_data='yes_balance')],
                [InlineKeyboardButton(text='❌ Пополнить позже', callback_data='no_balance')],
            ]
        )
        return balance_keyboard
    
    # Клавиатура на количество пополнения баланса
    async def amount_of_top_up(self) -> InlineKeyboardMarkup:
        balance_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='💰 100 рублей', callback_data='100_rub')],
                [InlineKeyboardButton(text='💰 150 рублей', callback_data='150_rub')],
                [InlineKeyboardButton(text='💰 500 рублей', callback_data='500_rub')],
                [InlineKeyboardButton(text='❌ Пополнить позже', callback_data='later')]
            ]
        )
        return balance_keyboard
    
    
    async def balance_options(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Пополнить на 50 рублей", callback_data="top_up_50"))
        keyboard.add(InlineKeyboardButton("Пополнить на 100 рублей", callback_data="top_up_100"))
        return keyboard
    
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
            inline_keyboard=[[InlineKeyboardButton(text='Далее', callback_data='I_agree')]])
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
    
    # Клавиатура чтобы сгенерировать описание
    async def generate_description(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='💰 5 руб.', callback_data='generate_description')],
            ]
        )
        return keyboard
    
    async def stay_reload_function(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Rewrite с теми же данными - 💰 3 руб (первые 3 бесплатно)', callback_data='reload')],
                    [InlineKeyboardButton(text='Оставить так', callback_data='stay')],
                ]
            )
        return select_keyboard
    
    async def change_parametrs(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Да, я хотел бы изменить некоторые параметры', callback_data='yes_change')],
                    [InlineKeyboardButton(text='Нет, не хочу менять', callback_data='no_change')],
                ]
            )
        return select_keyboard
    
    async def change_parameters_keyboard(self) -> InlineKeyboardMarkup:
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Количество комнат', callback_data='change_rooms')],
                [InlineKeyboardButton(text='Отделка квартиры', callback_data='change_renovation')],
                [InlineKeyboardButton(text='Стиль/ремонт квартиры', callback_data='change_style')],
                [InlineKeyboardButton(text='Совместимость кухни и гостиной', callback_data='change_kitchen')],
                [InlineKeyboardButton(text='Количество санузлов в квартире', callback_data='change_closet')],
                [InlineKeyboardButton(text='Количество спален в квартире', callback_data='change_bedrooms')],
                [InlineKeyboardButton(text='Санузел в спальне', callback_data='change_bedroom_wc')],
                [InlineKeyboardButton(text='Тип спальни', callback_data='change_bedroom_type')],
                [InlineKeyboardButton(text='Вид из спальни', callback_data='change_bedroom_view')],
                [InlineKeyboardButton(text='Вид из квартиры', callback_data='change_flat_view')],
                [InlineKeyboardButton(text='Площадь квартиры', callback_data='change_flat_area')],
                [InlineKeyboardButton(text='Изменить цену (Валюта не меняется)', callback_data='change_price')],
                [InlineKeyboardButton(text='Изменить достоинства квартиры', callback_data='change_flat_details')],
                [InlineKeyboardButton(text='Дополнительные комнаты', callback_data='change_extra_rooms')],
                [InlineKeyboardButton(text='ЖК с Циан / Дом', callback_data='change_jk_info')],
                [InlineKeyboardButton(text='Обязательная информация о квартире', callback_data='change_flat_extra_info')],
                [InlineKeyboardButton(text='Условия сделки', callback_data='change_deal_term')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back')]
            ]
        )
        return select_keyboard

    async def change_parameters_keyboard_one(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Количество комнат', callback_data='change_rooms')],
                [InlineKeyboardButton(text='Отделка квартиры', callback_data='change_renovation')],
                [InlineKeyboardButton(text='Стиль/ремонт квартиры', callback_data='change_style')],
                [InlineKeyboardButton(text='Совместимость кухни и гостиной', callback_data='change_kitchen')],
                [InlineKeyboardButton(text='Далее', callback_data='next_one')],
                [InlineKeyboardButton(text='К генерации описания', callback_data='change_back')]
            ])
            
        return select_keyboard
    
    async def change_parameters_keyboard_two(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Ремонт в квартире', callback_data='change_info_renovation')],
                [InlineKeyboardButton(text='ИНформацияо кухне/гостиной', callback_data='change_info_kitchen_living_room')],
                [InlineKeyboardButton(text='Количество санузлов в квартире', callback_data='change_closet')],
                [InlineKeyboardButton(text='Количество спален в квартире', callback_data='change_bedrooms')],
                [InlineKeyboardButton(text='Далее', callback_data='next_two')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back_two')]
            ])
            
        return select_keyboard

    async def change_parameters_keyboard_three(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                
                [InlineKeyboardButton(text='Вид из квартиры', callback_data='change_flat_view')],
                [InlineKeyboardButton(text='Площадь квартиры', callback_data='change_flat_area')],
                [InlineKeyboardButton(text='Изменить цену (Валюта не меняется)', callback_data='change_price')],
                [InlineKeyboardButton(text='Изменить достоинства квартиры', callback_data='change_flat_details')],
                
                [InlineKeyboardButton(text='Далее', callback_data='next_three')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back_three')]
            ])
            
        return select_keyboard
    
    async def change_parameters_keyboard_four(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Дополнительные комнаты', callback_data='change_extra_rooms')],
                [InlineKeyboardButton(text='Обязательная информация о квартире', callback_data='change_flat_extra_info')],
                [InlineKeyboardButton(text='Обязательная информация о ЖК/доме', callback_data= 'change_jk_extra_info')],
                [InlineKeyboardButton(text='Условия сделки', callback_data='change_deal_term')],
                [InlineKeyboardButton(text='Назад', callback_data='change_back_four')]
            ])
            
        return select_keyboard
    
    async def support_keyboard_chose(self) -> ReplyKeyboardMarkup:
        """
        Функция для построения кнопок в зависимости от уровня доступа
        """
        keyboard_reply_builder = ReplyKeyboardBuilder()
        keyboard_constructor = ['📨 Тех.поддержка / QA', '📚 Про нас / Вакансии', 'Вернуться к основным разделам']

        for button in keyboard_constructor:
            keyboard_reply_builder.add(KeyboardButton(text=button))

        return keyboard_reply_builder.adjust(2).as_markup(resize_keyboard=True)
    
    async def support_variant(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='📲 Q/A с Разработчиком', callback_data='developer_qa')],
                [InlineKeyboardButton(text='📲 Q/A c Руководителем', callback_data='seo_qa')],

            ])
            
        return select_keyboard
    
    async def support_options_developer(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='❓ Задать вопрос', callback_data='question')],
                [InlineKeyboardButton(text='💡 Поделиться идеей или улучшением', callback_data='idea')],
                [InlineKeyboardButton(text='Назад', callback_data='support_back')],
            ])
            
        return select_keyboard
    
    async def support_options_seo(self):
        select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='❓ Задать вопрос', callback_data='question_seo')],
                [InlineKeyboardButton(text='💡 Поделиться идеей или улучшением', callback_data='idea_seo')],
                [InlineKeyboardButton(text='Назад', callback_data='support_back_seo')],
            ])
            
        return select_keyboard
    
if __name__ == "__main__":
    kb = Custom_Keyboard()
    print(kb.main_keyboard)
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
