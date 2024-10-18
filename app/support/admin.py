import json
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.states import UserState
from database.orm_query import orm_add_action_with_ideas, orm_add_action_with_question, orm_delete_user_question, orm_get_all_ideas, orm_get_all_questions, orm_get_user_question
import keyboard.keyboard as kb
from aiogram.filters.command import Command
from config_reader import config
from app.support.support_state import SupportState
from aiogram.filters.command import CommandObject

support_router = Router()

SUPPORT_CHAT_ID = int(config.support_chat_id.get_secret_value())
BOT_CHAT_ID = int(config.bot_chat_id.get_secret_value())
print(SUPPORT_CHAT_ID)
print(BOT_CHAT_ID)

class AdminSupport:
    
    _user_names = None  # Класс-атрибут для хранения загруженных данных

    @classmethod
    async def load_user_names(cls):
        if cls._user_names is None:
            with open('database/user_names_for_access.json', encoding='UTF-8') as f:
                cls._user_names = json.load(f)

    @staticmethod
    @support_router.message(F.text.in_(["💌 Тех.поддержка / QA"]))
    async def handle_support_module(message: Message, state: FSMContext, session: AsyncSession):
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
            await message.answer(f'⚠️ Во время заполнения деталей квартиры НЕЛЬЗЯ связаться с поддержкой.\nВы рискуете потерять все данные!!!!\nДля работы с поддержкой либо перезапустите бот либо перезапустите режим Конструктора ❤️')

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
            await message.answer('Вас приветствует поддержка бота Дейл 🛠 \n\nПожалуйста выберите интересный вам раздел модуля поддержки 📝', reply_markup=await kb.Custom_Keyboard().support_keyboard_chose())

    @staticmethod
    @support_router.message(F.text.in_(["📨 Тех.поддержка / QA", '📚 Про нас / Вакансии', 'Вернуться к основным разделам']))
    async def handle_support_variant(message: Message, state: FSMContext, session: AsyncSession):
        if message.text == "📨 Тех.поддержка / QA":
            await message.answer('С кем бы вы хотели связаться и задать вопрос?', reply_markup=await kb.Custom_Keyboard().support_variant())
        elif message.text == '📚 Про нас / Вакансии':
            await message.answer('Мы лучшая компания недвижимости PEOPLE\n\nВсе актульные вакансии доступны по ссылке `https://hh.ru/employer/4683947`')
        elif message.text == 'Вернуться к основным разделам':
            await message.answer('Если возникнут идеи или появятся вопросы, обязательно пишите!', reply_markup=await kb.Custom_Keyboard().main_keyboard(message.from_user.username))

    @staticmethod
    @support_router.callback_query(F.data.in_(['developer_qa', 'seo_qa']))
    async def handle_kind_of_admins(call: CallbackQuery, state: FSMContext, session: AsyncSession):
        if call.data == 'developer_qa':
            await call.message.answer('Выберите действие:', reply_markup=await kb.Custom_Keyboard().support_options_developer())
        elif call.data == 'seo_qa':
            await call.message.answer('Выберите действие:', reply_markup=await kb.Custom_Keyboard().support_options_seo())

    @staticmethod
    @support_router.callback_query(F.data.in_(["question", 'idea', 'support_back']))
    async def handle_client_choosing(call: CallbackQuery, state: FSMContext, session: AsyncSession):
        if call.data == "question":
            await state.set_state(SupportState.question_to_developer)
            await call.message.answer('Пожалуйста сформулируйте грамотно свой вопрос и отправьте мне.\n\nЯ передам его и пришлю ответ в бот в течение одного дня ❤️')
        elif call.data == 'idea':
            await state.set_state(SupportState.idea_to_developer)
            await call.message.answer('Пожалуйста сформулируйте грамотно свою идею по улучшению старых функций или по добавлению новых фичей в бот❤️')
        elif call.data == 'support_back':
            await call.message.answer('С кем бы вы хотели связаться и задать вопрос?', reply_markup=await kb.Custom_Keyboard().support_variant())
    
    @staticmethod
    @support_router.message(SupportState.question_to_developer)
    async def handle_question_to_developer(message: Message, state: FSMContext, session: AsyncSession):
        
        await state.update_data(question_to_developer=message.text)
        await message.answer('Передал ваш вопрос! Ответ придет в бот в течение одного дня 💌\n\nС кем бы вы хотели связаться и задать вопрос?', reply_markup=await kb.Custom_Keyboard().support_variant())
        
        data = await state.get_data()
        to_admin_chat = f"✉ Новое уведомление от @{message.from_user.username}\n\nПользователь задал вопрос: {data['question_to_developer']}\n\nID пользователя для ответа: {message.message_id}"
        await AdminSupport.send_to_group(message, to_admin_chat)
        await orm_add_action_with_question(session=session, user_id=message.from_user.id,chat_id=message.chat.id, message_id=message.message_id, user_name=message.from_user.username,question=data['question_to_developer'], for_who='разработчик')

    @staticmethod
    @support_router.message(SupportState.idea_to_developer)
    async def handle_idea_to_developer(message: Message, state: FSMContext, session: AsyncSession):
        await state.update_data(idea_to_developer=message.text)
        await message.answer('Спасибо за вашу идею и обратную связь! Разработчики учтут все ваши наблюдения! 💌\n\nС кем бы вы хотели связаться и задать вопрос?', reply_markup=await kb.Custom_Keyboard().support_variant())
        
        data = await state.get_data()
        to_admin_chat = f"✉ Новое уведомление от @{message.from_user.username}\n\nПользователь прислал свою идею для улучшения: {data['idea_to_developer']}"
        await AdminSupport.send_to_group(message, to_admin_chat)
        await orm_add_action_with_ideas(session=session, user_id=message.from_user.id,chat_id=message.chat.id, user_name=message.from_user.username, idea=data['idea_to_developer'], for_who='разработчик')
        
    @staticmethod
    @support_router.callback_query(F.data.in_(["question_seo", 'idea_seo', 'support_back_seo']))
    async def handle_client_choosing_seo(call: CallbackQuery, state: FSMContext, session: AsyncSession):
        if call.data == "question_seo":
            await state.set_state(SupportState.question_to_seo)
            await call.message.answer('Пожалуйста сформулируйте грамотно свой вопрос и отправьте мне.\n\nЯ передам его и пришлю ответ в бот в течение одного дня ❤️')
        elif call.data == 'idea_seo':
            await state.set_state(SupportState.idea_to_seo)
            await call.message.answer('Пожалуйста сформулируйте грамотно свою идею по улучшению старых функций или по добавлению новых фичей в бот❤️')
        elif call.data == 'support_back_seo':
            await call.message.answer('С кем бы вы хотели связаться и задать вопрос?', reply_markup=await kb.Custom_Keyboard().support_variant())
    
    @staticmethod
    @support_router.message(SupportState.question_to_seo)
    async def handle_question_to_seo(message: Message, state: FSMContext, session: AsyncSession):
        await state.update_data(question_to_seo=message.text)
        await message.answer('Передал ваш вопрос! Ответ придет в бот в течение одного дня 💌\n\nС кем бы вы хотели связаться и задать вопрос?', reply_markup=await kb.Custom_Keyboard().support_variant())
        
        data = await state.get_data()
        to_admin_chat = f"✉ Новое уведомление от @{message.from_user.username}\n\nПользователь задал вопрос: {data['question_to_seo']}\n\nID пользователя для ответа: `{message.message_id}` ?"
        await AdminSupport.send_to_group(message, to_admin_chat)
        await orm_add_action_with_ideas(session=session, user_id=message.from_user.id,message_id=message.message_id, user_name=message.from_user.username, idea=data['question_to_seo'], for_who='руководитель')

    @staticmethod
    @support_router.message(SupportState.idea_to_seo)
    async def handle_idea_to_seo(message: Message, state: FSMContext, session: AsyncSession):
        await state.update_data(idea_to_seo=message.text)
        await message.answer('Спасибо за вашу идею и обратную связь! SEO внимательно ознакомятся с вашей идеей и доработают меня! 💌\n\nС кем бы вы хотели связаться и задать вопрос?', reply_markup=await kb.Custom_Keyboard().support_variant())
        
        data = await state.get_data()
        to_admin_chat = f"Новое уведомление от @{message.from_user.username}\n\nПользователь прислал свою идею для улучшения: {data['idea_to_seo']}"
        await AdminSupport.send_to_group(message, to_admin_chat)
        await orm_add_action_with_ideas(session=session, user_id=message.from_user.id, user_name=message.from_user.username, idea=data['idea_to_seo'], for_who='руководитель')
    
    @staticmethod
    async def send_to_group(message: Message, text: str, chat_id=SUPPORT_CHAT_ID):
        try:
            await message.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            await message.reply(f"Не удалось отправить сообщение: {e}")
        
    @staticmethod
    @support_router.message(Command("ответ"))
    async def start_reply(message: Message, command: CommandObject, state: FSMContext, session: AsyncSession):
        if message.chat.id == SUPPORT_CHAT_ID:
            
            command_args = command.args.split(maxsplit=1)
            if len(command_args) < 2:
                await message.answer('⚠ Укажите аргументы команды\nПример: `/ответ 516712732 Ваш ответ`')
                return

            original_message_id = int(command_args[0])
            chat_id, question = await orm_get_user_question(session=session,message_id=original_message_id) # получаем вопрос по id
            response_text = command_args[1]

            await message.bot.send_message(chat_id=chat_id, text=f"✉ Новое уведомление!\n\nВы ранее задали вопрос: \n\n`{question}`.\n\n Ответ от тех.поддержки:\n\n`{response_text}`", parse_mode='Markdown')
            await message.answer("Ваш ответ был отправлен! Спасибо!")
            await orm_delete_user_question(session=session, message_id=original_message_id) # удаляем вопрос после ответа
        else:
            await message.answer('Не тот чат')

    @staticmethod
    @support_router.message(Command("get_chat_id"))
    async def get_chat_id(message: Message, command: CommandObject):
        chat_id = message.chat.id
        await message.answer(f"ID этого чата: {chat_id}")

    # Отправка и получение из бд вопросов для руководителя и разработчику
    async def get_and_send_questions(message: Message, session: AsyncSession, for_who: str, allowed_users: list):
        
        if message.chat.id == SUPPORT_CHAT_ID and message.from_user.username in allowed_users:
            data = await orm_get_all_questions(session=session, for_who=for_who)
            for option in data:
                user_name, message_id, question = option
                await message.answer(f'Пользователь @{user_name} задал вопрос {for_who}у: `{question}`\n\nID для ответа Message ID: {message_id}')
        else:
            await message.answer("⚠ У вас нет доступа к этой функции. Хорошего дня ❤️")
    
    # Отправка и получение из бд идей для руководителя и разработчику
    async def get_and_send_ideas(message: Message, session: AsyncSession, for_who: str, allowed_users: list):
        
        if message.chat.id == SUPPORT_CHAT_ID and message.from_user.username in allowed_users:
            
            data = await orm_get_all_ideas(session=session, for_who=for_who)
            for option in data:
                user_name, idea  = option
                await message.answer(f'Пользователь @{user_name} прислал идею для {for_who}: `{idea}`\n\n')
        else:
            await message.answer("⚠ У вас нет доступа к этой функции. Хорошего дня ❤️")
    
    @staticmethod
    @support_router.message(Command("question_developer"))
    async def question_developer(message: Message, session: AsyncSession):
        
        await AdminSupport.load_user_names()
        
        await AdminSupport.get_and_send_questions(message, session, 'разработчик', AdminSupport._user_names['developer'])

    @staticmethod
    @support_router.message(Command("question_seo"))
    async def question_seo(message: Message, session: AsyncSession):
        
        await AdminSupport.load_user_names()
        
        await AdminSupport.get_and_send_questions(message, session, 'руководитель', AdminSupport._user_names['seo'])
        
    @staticmethod
    @support_router.message(Command("idea_developer"))
    async def idea_developer(message: Message, session: AsyncSession):
        await AdminSupport.load_user_names()
        await AdminSupport.get_and_send_ideas(message, session, 'разработчик', AdminSupport._user_names['developer'])

    @staticmethod
    @support_router.message(Command("idea_seo"))
    async def idea_seo(message: Message, session: AsyncSession):
        await AdminSupport.load_user_names()
        await AdminSupport.get_and_send_ideas(message, session, 'руководитель', AdminSupport._user_names['seo'])
    
    @staticmethod
    @support_router.message(Command("admin"))
    async def idea_seo(message: Message, session: AsyncSession):
        
        await AdminSupport.load_user_names()
            
        if message.from_user.username in AdminSupport._user_names['admin'] and message.chat.id == SUPPORT_CHAT_ID:
            
            await message.answer("УПРАВЛЕНИЕ ТЕХ.ПОДДЕРЖКОЙ:\n\n"
                    "КАК ОТВЕЧАТЬ НА ВОПРОС:\n"
                    "Шаблон:\n\n"
                    "/ответ ID_сообщения ВАШ_ОТВЕТ\n\n"
                    "Пример:\n\n"
                    "`/ответ 7589 Зайдите в раздел баланса и следуйте инструкции`\n\n"
                    "ВАЖНЫЕ ФУНКЦИИ (МОЖЕТЕ НАЖИМАТЬ ТО ЧТО ВАМ НУЖНО):\n\n"
                    "/question_developer - выведет все вопросы , которые требуют ответа и были заданы РАЗРАБОТЧИКУ\n\n"
                    " /question_seo - выведет все вопросы , которые требуют ответа и были заданы РУКОВОДИТЕЛЮ\n\n"
                    "/idea_developer - выведет все идеи , которые были предложены РАЗРАБОТЧИКУ\n\n"
                    "/idea_seo - выведет все идеи , которые были предложены РУКОВОДИТЕЛЮ\n\n"
                    "ЧТО-ТО ЗАБЫЛИ - СМОТРИ ЗАКРЕП ❤️")
        else:
            await message.answer('⚠ Вы не являетесь админом или разработчиком. Если вы админ или разработчик, проверьте в правильном ли вы чатике ❤️')