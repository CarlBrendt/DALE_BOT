from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.states import UserState
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import keyboard.keyboard as kb  # предполагается, что в этом модуле у вас определены функции создания клавиатур

changing_parameters_router = Router()

class ChangeParam:

    @staticmethod
    @changing_parameters_router.callback_query(F.data.in_(['yes_change', 'no_change']))
    async def handle_changes(callback: CallbackQuery, state: FSMContext):
        if callback.data == 'yes_change':
            await callback.message.answer('Выберите параметр, который хотите изменить', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_one())
            await state.set_state(UserState.changing_parameters)
        elif callback.data == 'no_change':
            await callback.message.answer('Сгенерировать описание + 3 рерайта описания', reply_markup=await kb.Custom_Keyboard().generate_description())

    @staticmethod
    @changing_parameters_router.callback_query(UserState.changing_parameters, F.data)
    async def handle_parameter_selection(callback: CallbackQuery, state: FSMContext):
        parameter_map = {
            'change_info_renovation': UserState.info_about_renovation,
            'change_rooms': UserState.number_of_rooms,
            'change_renovation': UserState.renovation_status,
            'change_style': UserState.style,
            'change_kitchen': UserState.kitchen_living_room,
            'change_closet': UserState.number_of_closet,
            'change_bedrooms': UserState.number_of_bedrooms,
            'change_bedroom_wc': UserState.bedroom_wc,
            'change_bedroom_type': UserState.bedroom_type,
            'change_bedroom_view': UserState.bedroom_view,
            'change_flat_view': UserState.flat_view,
            'change_flat_area': UserState.flat_area,
            'change_price': UserState.price_int,
            'change_flat_details': UserState.flat_details,
            'change_jk_info': UserState.jk_info_yes_or_no,
            'change_extra_rooms': UserState.info_about_extra_rooms,
            'change_flat_extra_info': UserState.flat_extra_info,
            'change_deal_term': UserState.deal_term,
            'change_jk_extra_info': UserState.jk_extra_info,
            'change_info_kitchen_living_room': UserState.info_about_kitchen_living_room
        }

        if callback.data == 'change_back':
            await callback.message.answer('Сгенерировать описание + 3 рерайта описания', reply_markup=await kb.Custom_Keyboard().generate_description())
        elif callback.data == 'next_one':
            await callback.message.edit_text('Выберите параметр, который хотите изменить', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_two())
        elif callback.data == 'change_back_two':
            await callback.message.edit_text('Выберите параметр, который хотите изменить', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_one())
        elif callback.data == 'next_two':
            await callback.message.edit_text('Выберите параметр, который хотите изменить', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_three())
        elif callback.data == 'change_back_three':
            await callback.message.edit_text('Выберите параметр, который хотите изменить', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_two())
        elif callback.data == 'next_three':
            await callback.message.edit_text('Выберите параметр, который хотите изменить', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_four())
        elif callback.data == 'change_back_four':
            await callback.message.edit_text('Выберите параметр, который хотите изменить', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_three())
        else:
            new_state = parameter_map.get(callback.data)
            if new_state:
                await state.update_data(last_state=new_state)  # сохраняем состояние для возврата
                await state.set_state(UserState.awaiting_new_value)
                await ChangeParam.send_current_question(callback.message, new_state, state)

    @staticmethod
    async def send_current_question(message: Message, state_name: str, state: FSMContext):
        questions_map = {
            UserState.number_of_rooms: 'Пожалуйста выберите количество комнат в квартире',
            UserState.renovation_status: 'Квартира с отделкой или без?',
            UserState.style: 'Пожалуйста введите стиль, в котором оформлена ваша квартира\n\nПримеры:\n1 пример - модерн\n2 пример - моя квартира в стиле eclectic\n3 пример - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!',
            UserState.kitchen_living_room: 'Кухня совмещена с гостиной?',
            UserState.number_of_closet: 'Сколько санузлов во ВСЕЙ квартире?',
            UserState.number_of_bedrooms: 'Сколько спален в вашей квартире?',
            UserState.info_about_renovation: 'Пожалуйста расскажите о ремонте/мебели ВО ВСЕЙ квартире\n\nПример 1 - паркет из красного дуба, итальянская мебель ручной работы\nПример 2 - отделка потолка и пола в стиле LV, над дизайном работал знаменитый японский дизайнер\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!',
            UserState.info_about_kitchen_living_room: 'Расскажите об интересных деталях кухни и гостиной. При желании можно указать площадь\n\nПример 1 - В кухне есть посудомойки от Bosh , гостиная полностью мебелирована\nПример 2 - Площадь гостиной - 20 м2 , есть ниша под телевизор\nПример 3 - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!',
            UserState.bedroom_wc: 'В этой спальне свой санузел?',
            UserState.bedroom_type: 'Какой тип этой спальни?',
            UserState.bedroom_view: 'Опишите вид из этой спальни',
            UserState.flat_view: 'Опишите куда выходят окна квартиры(виды). НЕ ОПИСЫВАЙТЕ ВИДЫ ИЗ СПАЛЕН!!!!!\n\nПример 1 - Панорамные окна выходят на Савинскую набережную\nПример 2 - видно кремль как на ладони\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!',
            UserState.flat_area: 'Укажите общую площадь квартиры\n\nПример 1 - 57,2\nПример 2 - 68\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!',
            UserState.price_int: 'Пожалуйста введите цену в следующем формате\n\nПример 1 - 120 000 000\nПример 2 - 258 900 000\nПример 3 - Договорная',
            UserState.flat_details: 'Расскажите кратко о достоинствах и плюсах квартиры\n\nПример 1 - До центра 10 минут, три парка рядом, в доме 4 ресторана\nПример 2 - В стоимость входит 2 м\м, Видно москву сити, до метро 2 минуты, консьерж\nПример 3 - я не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ !!',
            UserState.jk_info_yes_or_no: 'Прежде чем я буду брать информацию о вашем ЖК/доме с сайта ЦИАН, не могли бы вы уточнить есть ли информация на ЦИАН о вашем ЖК/доме?',
            UserState.info_about_extra_rooms: 'Если в вашей квартире есть дополнительные комнаты, то перечислите их\n\nПример 1 - нет таких/нет\nПример 2 - есть постирочная, гардеробная, балкон\nПример 3 - лоджия, гардеробная\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!',
            UserState.flat_extra_info: "Пожалуйста укажите информацию, которую мне стоит ОБЯЗАТЕЛЬНО учесть и включить в описание квартиры\n\nПример 1 - в квартире проживал знаменитый актер, в квартире разрешен снос межкомнатных стен\nПример 2 - не знаю\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!",
            UserState.jk_extra_info: 'Здесь вы можете ввести информацию, которую ОБЯЗАТЕЛЬНО хотели бы учесть при формировании описания ЖК/дома\n\nПример 1 - дом построен в 1957 году, в нем жил знаменитый актер\nПример 2 - нет такой\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!',
            UserState.deal_term: 'Расскажите об условиях сделки. УКАЗАТЬ ОБЯЗАТЕЛЬНО\n\nПример 1 - 1 взрослый собственник, прямая продажа\nПример 2 - Торг, готовы выслушать ваше предложение по цене, Дизайн проект в подарок\n\nВВОД ОСУЩЕСТВЛЯЕТСЯ С КЛАВИАТУРЫ ТЕКСТОМ КАК В ПРИМЕРАХ!!'
        }
        keyboards_map = {
            UserState.number_of_rooms: await kb.Custom_Keyboard().rooms_select_keyboard(),
            UserState.renovation_status: await kb.Custom_Keyboard().select_renovation_keyboard(),
            UserState.kitchen_living_room: await kb.Custom_Keyboard().kitchen_with_living_room_keyboard(),
            UserState.number_of_closet: await kb.Custom_Keyboard().wc_select_keyboard(),
            UserState.price: await kb.Custom_Keyboard().type_of_price(),
            UserState.bedroom_wc: await kb.Custom_Keyboard().number_of_wc_in_bedroom(),
            UserState.bedroom_type: await kb.Custom_Keyboard().type_of_bedroom(),
            UserState.changing_parameters: await kb.Custom_Keyboard().change_parameters_keyboard_one()  # Начальная клавиатура
        }

        question = questions_map.get(state_name, 'Введите новое значение:')
        keyboard = keyboards_map.get(state_name, None)

        await message.answer(question, reply_markup=keyboard)

    @staticmethod
    @changing_parameters_router.message(UserState.awaiting_new_value)
    async def handle_new_parameter_value(message: Message, state: FSMContext, session: AsyncSession):
        await ChangeParam.save_new_value(message.text, state)
        await message.answer('Параметр успешно обновлен. Хотите изменить еще что-нибудь?', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_one())
        await state.set_state(UserState.changing_parameters)

    @staticmethod
    @changing_parameters_router.callback_query(UserState.awaiting_new_value, F.data)
    async def handle_new_parameter_value_callback(callback: CallbackQuery, state: FSMContext):
        await ChangeParam.save_new_value(callback.data, state)
        await callback.message.answer('Параметр успешно обновлен. Хотите изменить еще что-нибудь?', reply_markup=await kb.Custom_Keyboard().change_parameters_keyboard_one())
        await state.set_state(UserState.changing_parameters)

    @staticmethod
    async def save_new_value(value, state: FSMContext):
        data = await state.get_data()
        last_state = data.get('last_state', UserState.changing_parameters)

        update_data_map = {
            UserState.info_about_renovation: 'info_about_renovation',
            UserState.number_of_rooms: 'number_of_rooms',
            UserState.renovation_status: 'renovation_status',
            UserState.style: 'style',
            UserState.kitchen_living_room: 'kitchen_living_room',
            UserState.number_of_closet: 'number_of_closet',
            UserState.number_of_bedrooms: 'number_of_bedrooms',
            UserState.bedroom_wc: 'bedroom_wc',
            UserState.bedroom_type: 'bedroom_type',
            UserState.bedroom_view: 'bedroom_view',
            UserState.flat_view: 'flat_view',
            UserState.flat_area: 'flat_area',
            UserState.price_int: 'price',
            UserState.flat_details: 'flat_details',
            UserState.jk_info_yes_or_no: 'jk_info_yes_or_no',
            UserState.info_about_extra_rooms: 'info_about_extra_rooms',
            UserState.flat_extra_info: 'flat_extra_info',
            UserState.deal_term: 'deal_term',
            UserState.jk_extra_info: 'change_jk_extra_info',
            UserState.info_about_kitchen_living_room: 'change_info_kitchen_living_room'
            
        }

        if last_state in update_data_map:
            await state.update_data({update_data_map[last_state]: value})
        else:
            raise ValueError('Unknown state for updating parameter.')

