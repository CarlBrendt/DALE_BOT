import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from app.description_constructor.description_constuctor_handler import router
from main_router import main_router
from app.middleware import TestMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from app.description_constructor.load_cian_text import main 
from app.description_constructor.gpt_usage import main_gpt
from app.description_constructor.description_with_gpt import create_unique_description_of_building

# Для записей с типом Secret* необходимо 
# вызывать метод get_secret_value(), 
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())

# Диспетчер
dp = Dispatcher()
# Настройка RedisStorage
#redis_url = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
#storage = RedisStorage.from_url(redis_url)
dp = Dispatcher(storage=MemoryStorage())

# кнопка меню слева снизу
async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/start", description="Запуск/Перезапуск бота"),
        BotCommand(command="/status", description="Вывод информации из конструктора описания квартир"),
        BotCommand(command="/help", description="Помощь и инструкции")
    ]
    await bot.set_my_commands(bot_commands)

# Запуск процесса поллинга новых апдейтов
async def main_1():
    dp.include_routers(main_router, router)
    dp.message.outer_middleware(TestMiddleware())
    dp.startup.register(setup_bot_commands)
    #dp.message.register(cmd_test2, Command("test2"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    
    #asyncio.run(create_unique_description_of_building('https://zhk-skyview-i.cian.ru/'))
    
    try:
        asyncio.run(main_1())
    except KeyboardInterrupt:
        print('Exit from Bot')