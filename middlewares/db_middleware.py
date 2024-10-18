<<<<<<< HEAD
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

class DataBaseSession(BaseMiddleware):
    
    def __init__(self, session_pool: async_sessionmaker) -> None:
        self.session_pool = session_pool
        
    async def __call__(self, 
                    handler: Callable[[TelegramObject, Dict[str, Any]],
                    Awaitable[Any]], event: TelegramObject,
                    data: Dict[str, Any]) -> Any:
        
            async with self.session_pool() as session:
                data['session'] = session
=======
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

class DataBaseSession(BaseMiddleware):
    
    def __init__(self, session_pool: async_sessionmaker) -> None:
        self.session_pool = session_pool
        
    async def __call__(self, 
                    handler: Callable[[TelegramObject, Dict[str, Any]],
                    Awaitable[Any]], event: TelegramObject,
                    data: Dict[str, Any]) -> Any:
        
            async with self.session_pool() as session:
                data['session'] = session
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
                return await handler(event, data)