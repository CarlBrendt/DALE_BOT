<<<<<<< HEAD
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
import os
from database.models import Base
from config_reader import config
import asyncpg

os.environ['DATABASE'] = config.db_url.get_secret_value()
DATABASE = os.environ.get('DATABASE')

uri = os.getenv("DATABASE")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+asyncpg://", 1)

# postgresql+asyncpg://server_name:password@host:port/dbname
engine = create_async_engine(url=uri, echo=True, connect_args={"ssl": "require"})

# асинхронная сесия для добавлени в бд
session_maker = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

# создание базы данных
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
# удаление базы данных
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
=======
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
import os
from database.models import Base
from config_reader import config
import asyncpg

os.environ['DATABASE'] = config.db_url.get_secret_value()
DATABASE = os.environ.get('DATABASE')

uri = os.getenv("DATABASE")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+asyncpg://", 1)

# postgresql+asyncpg://server_name:password@host:port/dbname
engine = create_async_engine(url=uri, echo=True, connect_args={"ssl": "require"})

# асинхронная сесия для добавлени в бд
session_maker = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

# создание базы данных
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
# удаление базы данных
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
