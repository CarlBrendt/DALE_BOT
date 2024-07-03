from aiogram.fsm.state import StatesGroup, State

# класс ответов пользователей
class UserState(StatesGroup):

    last_question = State() # последний вопрос пользователю для возвращения после выбора status
    last_keyboard = State() # последняя клавиатура для пользователя для возвращения после выбора status
    number_of_rooms = State() # количество комнат
    waiting_for_room_count = State() # ручной ввод числа комнат
    renovation_status = State() # есть ли отделка
    style = State() # стиль квартиры
    kitchen_living_room = State() # совмещена ли кухня с гостинной
    number_of_closet = State() # количество санузлов
    waiting_for_closet_count = State() # ждем когда пользователь введет количество туалетов
    number_of_bedrooms = State() # количество спален в квартире
    waiting_for_bedrooms_count = State() # ждем когда пользователь введет количество спален вручную
    info_bed = State() # информация о каждой спальни
    bedroom_area = State() # площадь каждой спальни
    bedroom_wc = State() # есть ли туалет в спальне
    bedroom_type = State() # тип каждой спальни 
    bedroom_view = State() # вид из каждой спальни
    bedroom_details = State() # детали спальни, например итальянская мебель, зеркала ручной работы в спальне
    flat_view = State() # виды из окон квартира , не считая спален
    price = State() # спрашиваем валюту
    flat_area = State() # спрашиваем общую площадь
    price_int = State() # пользователь вводит цену вручную
    flat_details = State() # достоинства и плюсы квартиры
    link_house = State() # ссылка на циан жк
    test = State() # просто для проверки статуса, то есть что ввели 
    pay = State() # подключаем оплату
    info_about_extra_rooms = State() # информацию о дополнительных комнатах
    jk_info_yes_or_no = State() # мы спрашиваем у пользователя есть ли информация на сайте циана о жк
    jk_written_info = State() # пользователь вручную вводит инфо о жк вручную
    jk_extra_info = State() # ОБЯЗАТЕЛЬНАЯ ИНФОРМАЦИЯ О ЖК
    flat_extra_info = State() # ОБЯЗАТЕЛЬНАЯ ИНФОРМАЦИЯ О КВАРТИРЕ
    unique_description_of_building = State() # описание жк после gpt
    deal_term = State() # условия сделки
    flat_text = State() # описание квартиры
    description_ready = State() # описание квартиры готово
    