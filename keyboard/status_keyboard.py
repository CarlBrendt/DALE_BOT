from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Custom_Status_Keyboard:
    
        async def choose_template_first(self):
            select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Первый шаблон', callback_data='first_template')],
                [InlineKeyboardButton(text='Второй шаблон', callback_data='second_template')],
                [InlineKeyboardButton(text='Третий шаблон', callback_data='third_template')],
                [InlineKeyboardButton(text='Далее', callback_data='forward_template')],
            ])
            
            return select_keyboard
        
        async def choose_template_second(self):
            select_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Четвертый шаблон', callback_data='fourth_template')],
                [InlineKeyboardButton(text='Пятый шаблон', callback_data='fifth_template')],
                [InlineKeyboardButton(text='Шестой шаблон', callback_data='six_template')],
                [InlineKeyboardButton(text='Назад', callback_data='back_template')],
            ])
            
            return select_keyboard
        
        @staticmethod
        async def get_template():
            select_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Получить готовый статус',callback_data="get_template")],
                ]
            )
            return select_keyboard