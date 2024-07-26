import asyncio
from aiogram import Bot, Dispatcher
from app.description_constructor.description_with_gpt import create_unique_description_of_building
from config_reader import config
from app.description_constructor.description_constuctor_handler import router
from app.description_constructor.change_parametrs_of_flat_handlers import changing_parameters_router
from database.engine import create_db, drop_db, session_maker
from main_router import main_router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from middlewares.db_middleware import DataBaseSession
from app.balance_constructor.balance_handlers import balance_router
from app.support.admin import support_router

# Для записей с типом Secret* необходимо 
# вызывать метод get_secret_value(), 
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())

# Настройка RedisStorage
#redis_url = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
#storage = RedisStorage.from_url(redis_url)
dp = Dispatcher(storage=MemoryStorage())

# кнопка меню слева снизу
async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/start", description="Запуск/Перезапуск бота"),
        BotCommand(command="/status", description="Вывод информации из конструктора описания квартир"),
        BotCommand(command='/admin', description='Доступна только для админов и разработчиков')
    ]
    await bot.set_my_commands(bot_commands)


async def on_startup():
    
    run_params = False
    
    if run_params:
        await drop_db()
        
    await create_db()

async def on_shutdown():
    print('Bot умер')

        
# Запуск процесса поллинга новых апдейтов
async def main_1():
    
    dp.include_router(main_router)
    #dp.include_router(balance_router)
    dp.include_router(support_router)

    dp.include_router(router)
    dp.include_router(changing_parameters_router)
    dp.update.outer_middleware(DataBaseSession(session_pool=session_maker))

    dp.startup.register(setup_bot_commands)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)
    
if __name__ == "__main__":
    
    try:
        asyncio.run(main_1())
    except KeyboardInterrupt:
        print('Exit from Bot')