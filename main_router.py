<<<<<<< HEAD
from aiogram import  types, Router
from aiogram.filters.command import CommandStart
import keyboard.keyboard as kb
from all_config import config as cf
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from database.orm_query import orm_register_or_update_user
from config_reader import config

main_router = Router()

SUPPORT_CHAT_ID = int(config.support_chat_id.get_secret_value())

# Хэндлер на команду /start
@main_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, session: AsyncSession):
        if message.chat.id != SUPPORT_CHAT_ID:
                await state.clear()
                await orm_register_or_update_user(session, message.from_user.id, message.from_user.username)
                await message.answer(f"{cf.text_greting}", reply_markup=await kb.Custom_Keyboard().main_keyboard(message.from_user.username))
        else:
=======
from aiogram import  types, Router
from aiogram.filters.command import CommandStart
import keyboard.keyboard as kb
from all_config import config as cf
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from database.orm_query import orm_register_or_update_user
from config_reader import config

main_router = Router()

SUPPORT_CHAT_ID = int(config.support_chat_id.get_secret_value())

# Хэндлер на команду /start
@main_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, session: AsyncSession):
        if message.chat.id != SUPPORT_CHAT_ID:
                await state.clear()
                await orm_register_or_update_user(session, message.from_user.id, message.from_user.username)
                await message.answer(f"{cf.text_greting}", reply_markup=await kb.Custom_Keyboard().main_keyboard(message.from_user.username))
        else:
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
                await message.answer('Не надо запускать здесь ботика 🥺\n\nЭто поддержка , здесь можно пользоваться /admin')