from aiogram import  types, Router
from aiogram.filters.command import CommandStart
import keyboard.keyboard as kb
from all_config import config as cf
from aiogram.fsm.context import FSMContext

main_router = Router()

# Хэндлер на команду /start
@main_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(f"{cf.text_greting}", reply_markup=await kb.Custom_Keyboard().main_keyboard(message.from_user.username))
        
        