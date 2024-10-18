<<<<<<< HEAD
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from app.states import UserState
import keyboard.keyboard as kb
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_user_balance, orm_update_users_balance, orm_add_action_with_top_up
from config_reader import config

balance_router = Router()
PAYMENT_TOKEN_TEST = config.payment_token_test.get_secret_value()

class BalanceHandler:

    @staticmethod
    @balance_router.message(F.text.in_(["💸 Баланс"]))
    async def handle_balance(message: Message, state: FSMContext, session: AsyncSession):
        current_state = await state.get_state()

        constructor_states = [
            UserState.number_of_rooms,
            UserState.renovation_status,
            UserState.waiting_for_room_count,
            UserState.style,
            UserState.info_about_renovation,
            UserState.kitchen_living_room,
            UserState.info_about_kitchen_living_room,
            UserState.number_of_closet,
            UserState.number_of_bedrooms,
            UserState.waiting_for_bedrooms_count,
            UserState.info_bed,
            UserState.bedroom_area,
            UserState.bedroom_wc,
            UserState.bedroom_type,
            UserState.bedroom_view,
            UserState.bedroom_details,
            UserState.flat_view,
            UserState.flat_area,
            UserState.price,
            UserState.price_int,
            UserState.flat_details,
            UserState.link_house,
            UserState.jk_info_yes_or_no,
            UserState.jk_extra_info,
            UserState.jk_written_info,
            UserState.info_about_extra_rooms,
            UserState.flat_extra_info,
            UserState.deal_term,
            UserState.description_ready
        ]
        
        if current_state in constructor_states:
            await message.answer(f'⚠️ Во время заполнения деталей квартиры НЕЛЬЗЯ пополнить баланс.\nВы рискуете потерять все данные!!!!\n\nБот сам оповестит вас, когда будет необходимо пополнить 💰 Баланс\nЕсли вы сами хотите пополнить баланс то перезапустите бота или перезапустите конструктор описания ❤️')
            
            data = await state.get_data()
            last_question = data.get('last_question', None)
            last_keyboard = data.get('last_keyboard', None)

            if last_question:
                if last_keyboard:
                    await message.answer(last_question, reply_markup=last_keyboard)
                else:
                    await message.answer(last_question)
            
            await state.set_state(current_state)  # Возвращаем пользователя к предыдущему состоянию
        else:
            await state.clear()  # Очищаем состояние перед выполнением операций с балансом
            balance = await orm_get_user_balance(session, message.from_user.id)
            await message.answer(f'Ваш баланс составляет {balance} руб. Хотели бы его пополнить?', 
                                parse_mode='Markdown',
                                reply_markup=await kb.Custom_Keyboard().upprove_balance())

    @staticmethod
    async def add_balance(call: CallbackQuery, amount: int):
        await call.bot.send_invoice(
            chat_id=call.from_user.id,
            title='Пополнить баланс',
            description='Пополнение баланса',
            provider_token=PAYMENT_TOKEN_TEST,
            payload='add_balance',
            currency='rub',
            prices=[
                LabeledPrice(
                    label=f'Пополнить баланс на {amount} рублей',
                    amount=amount * 100
                )
            ],
            start_parameter='People_test',
            need_phone_number=False
        )

    @staticmethod
    @balance_router.pre_checkout_query()
    async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @staticmethod
    @balance_router.message(F.successful_payment)
    async def successful_payment_handler(message: Message, session: AsyncSession, state: FSMContext):
        
        amount = message.successful_payment.total_amount // 100
        user_id = message.from_user.id
        balance_from_db = await orm_get_user_balance(session, user_id)
        current_balance = balance_from_db + amount
        await orm_update_users_balance(session=session, current_balance=current_balance, user_id=user_id)
        await message.answer(f'Вы успешно пополнили баланс. Текущий баланс составляет {current_balance} руб.\nХотите еще раз пополнить баланс?', 
                            reply_markup=await kb.Custom_Keyboard().upprove_balance())
        await orm_add_action_with_top_up(session=session, user_id=user_id, user_name=message.from_user.username, action=f'Пополнен баланс на +{amount}', top_up_amount=amount)

    @staticmethod
    @balance_router.callback_query(F.data.in_(["yes_balance", "no_balance"]))
    async def handle_grow_balance(call_query: CallbackQuery, session: AsyncSession):

        if call_query.data == 'yes_balance':
            await call_query.message.edit_text('Выберите сумму для пополения', reply_markup=await kb.Custom_Keyboard().amount_of_top_up())
        elif call_query.data == 'no_balance':
            await call_query.message.answer('Хорошо, если захотите пополнить баланс, обращайтесь!')

    @staticmethod
    @balance_router.callback_query(F.data.in_(["150_rub", "100_rub", "500_rub", "later"]))
    async def handle_amount_top_up(call_query: CallbackQuery, session: AsyncSession, state: FSMContext):

        if call_query.data == '150_rub':
            await BalanceHandler.add_balance(call_query, amount=150)
        elif call_query.data == '100_rub':
            await BalanceHandler.add_balance(call_query, amount=100)
        elif call_query.data == '500_rub':
            await BalanceHandler.add_balance(call_query, amount=500)
        elif call_query.data == 'later':
            balance = await orm_get_user_balance(session, call_query.from_user.id)
            await call_query.message.answer(f'Ваш баланс составляет {balance} руб. Хотели бы его пополнить?', 
                                            parse_mode='Markdown',
                                            reply_markup=await kb.Custom_Keyboard().upprove_balance())
=======
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from app.states import UserState
import keyboard.keyboard as kb
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_user_balance, orm_update_users_balance, orm_add_action_with_top_up
from config_reader import config

balance_router = Router()
PAYMENT_TOKEN_TEST = config.payment_token_test.get_secret_value()

class BalanceHandler:

    @staticmethod
    @balance_router.message(F.text.in_(["💸 Баланс"]))
    async def handle_balance(message: Message, state: FSMContext, session: AsyncSession):
        current_state = await state.get_state()

        constructor_states = [
            UserState.number_of_rooms,
            UserState.renovation_status,
            UserState.waiting_for_room_count,
            UserState.style,
            UserState.info_about_renovation,
            UserState.kitchen_living_room,
            UserState.info_about_kitchen_living_room,
            UserState.number_of_closet,
            UserState.number_of_bedrooms,
            UserState.waiting_for_bedrooms_count,
            UserState.info_bed,
            UserState.bedroom_area,
            UserState.bedroom_wc,
            UserState.bedroom_type,
            UserState.bedroom_view,
            UserState.bedroom_details,
            UserState.flat_view,
            UserState.flat_area,
            UserState.price,
            UserState.price_int,
            UserState.flat_details,
            UserState.link_house,
            UserState.jk_info_yes_or_no,
            UserState.jk_extra_info,
            UserState.jk_written_info,
            UserState.info_about_extra_rooms,
            UserState.flat_extra_info,
            UserState.deal_term,
            UserState.description_ready
        ]
        
        if current_state in constructor_states:
            await message.answer(f'⚠️ Во время заполнения деталей квартиры НЕЛЬЗЯ пополнить баланс.\nВы рискуете потерять все данные!!!!\n\nБот сам оповестит вас, когда будет необходимо пополнить 💰 Баланс\nЕсли вы сами хотите пополнить баланс то перезапустите бота или перезапустите конструктор описания ❤️')
            
            data = await state.get_data()
            last_question = data.get('last_question', None)
            last_keyboard = data.get('last_keyboard', None)

            if last_question:
                if last_keyboard:
                    await message.answer(last_question, reply_markup=last_keyboard)
                else:
                    await message.answer(last_question)
            
            await state.set_state(current_state)  # Возвращаем пользователя к предыдущему состоянию
        else:
            await state.clear()  # Очищаем состояние перед выполнением операций с балансом
            balance = await orm_get_user_balance(session, message.from_user.id)
            await message.answer(f'Ваш баланс составляет {balance} руб. Хотели бы его пополнить?', 
                                parse_mode='Markdown',
                                reply_markup=await kb.Custom_Keyboard().upprove_balance())

    @staticmethod
    async def add_balance(call: CallbackQuery, amount: int):
        await call.bot.send_invoice(
            chat_id=call.from_user.id,
            title='Пополнить баланс',
            description='Пополнение баланса',
            provider_token=PAYMENT_TOKEN_TEST,
            payload='add_balance',
            currency='rub',
            prices=[
                LabeledPrice(
                    label=f'Пополнить баланс на {amount} рублей',
                    amount=amount * 100
                )
            ],
            start_parameter='People_test',
            need_phone_number=False
        )

    @staticmethod
    @balance_router.pre_checkout_query()
    async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @staticmethod
    @balance_router.message(F.successful_payment)
    async def successful_payment_handler(message: Message, session: AsyncSession, state: FSMContext):
        
        amount = message.successful_payment.total_amount // 100
        user_id = message.from_user.id
        balance_from_db = await orm_get_user_balance(session, user_id)
        current_balance = balance_from_db + amount
        await orm_update_users_balance(session=session, current_balance=current_balance, user_id=user_id)
        await message.answer(f'Вы успешно пополнили баланс. Текущий баланс составляет {current_balance} руб.\nХотите еще раз пополнить баланс?', 
                            reply_markup=await kb.Custom_Keyboard().upprove_balance())
        await orm_add_action_with_top_up(session=session, user_id=user_id, user_name=message.from_user.username, action=f'Пополнен баланс на +{amount}', top_up_amount=amount)

    @staticmethod
    @balance_router.callback_query(F.data.in_(["yes_balance", "no_balance"]))
    async def handle_grow_balance(call_query: CallbackQuery, session: AsyncSession):

        if call_query.data == 'yes_balance':
            await call_query.message.edit_text('Выберите сумму для пополения', reply_markup=await kb.Custom_Keyboard().amount_of_top_up())
        elif call_query.data == 'no_balance':
            await call_query.message.answer('Хорошо, если захотите пополнить баланс, обращайтесь!')

    @staticmethod
    @balance_router.callback_query(F.data.in_(["150_rub", "100_rub", "500_rub", "later"]))
    async def handle_amount_top_up(call_query: CallbackQuery, session: AsyncSession, state: FSMContext):

        if call_query.data == '150_rub':
            await BalanceHandler.add_balance(call_query, amount=150)
        elif call_query.data == '100_rub':
            await BalanceHandler.add_balance(call_query, amount=100)
        elif call_query.data == '500_rub':
            await BalanceHandler.add_balance(call_query, amount=500)
        elif call_query.data == 'later':
            balance = await orm_get_user_balance(session, call_query.from_user.id)
            await call_query.message.answer(f'Ваш баланс составляет {balance} руб. Хотели бы его пополнить?', 
                                            parse_mode='Markdown',
                                            reply_markup=await kb.Custom_Keyboard().upprove_balance())
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
