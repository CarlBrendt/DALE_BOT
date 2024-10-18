from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import String, DateTime, Integer, BigInteger
from sqlalchemy import func


class Base(AsyncAttrs, DeclarativeBase):
    
    created_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now()) # время создания записи
    updated_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now()) # время обновления записи


# класс с балансом конкретного пользователя
class User(Base):
    
    __tablename__ = 'users_info'
    
    id: Mapped[int] = mapped_column(BigInteger,primary_key=True) # уникальное значение primary key, то есть у нас уникальные id пользователей
    user_name: Mapped[str] = mapped_column(String, nullable=False) # уникальное имя
    balance: Mapped[float] = mapped_column(Integer, nullable=False) # баланс пользователя

# класс для информации о поплнении баланса
class UserBalanceAction(Base):
    
    __tablename__ = 'action_with_balance'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) # уникальное значение primary key
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False) # ID пользователя
    user_name: Mapped[str] = mapped_column(String, nullable=False) # уникальное имя
    action: Mapped[str] = mapped_column(String, nullable=False) # что сделал пользователь с балансом
    top_up_balance_amount: Mapped[int] = mapped_column(Integer, nullable=False) # на сколько он пополнил баланс
    
class Questions(Base):
    __tablename__ = 'bot_questions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # уникальное значение primary key
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)  # ID пользователя
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)  # Chat ID пользователя
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)  # ID самого вопроса
    user_name: Mapped[str] = mapped_column(String, nullable=False)  # уникальное имя
    question: Mapped[str] = mapped_column(String, nullable=False)  # какой у пользователя вопрос
    for_who: Mapped[str] = mapped_column(String, nullable=False)  # для кого предназначается вопрос

class Ideas(Base):
    __tablename__ = 'bot_ideas'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # уникальное значение primary key
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)  # ID пользователя
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)  # Chat ID пользователя
    user_name: Mapped[str] = mapped_column(String, nullable=False)  # уникальное имя
    idea: Mapped[str] = mapped_column(String, nullable=False)  # какая у пользователя идея
    for_who: Mapped[str] = mapped_column(String, nullable=False)  # для кого предназначается идея
