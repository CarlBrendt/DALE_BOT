from sqlalchemy import delete, update
from database.models import Ideas, Questions, User, UserBalanceAction

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Функция для регистрации или обновления пользователя в базе данных
async def orm_register_or_update_user(session: AsyncSession, user_id: int, username: str):
    try:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if user:
            user.user_name = username
            # balance не изменяется при обновлении
        else:
            user = User(
                id=user_id,
                user_name=username,
                balance=0
            )
            session.add(user)

        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка при обновлении/регистрации пользователя: {e}")

# Функция для получения всех данных из нашей бд пользователей
async def orm_get_all_data(session: AsyncSession):
    query = select(User)
    result = await session.execute.all(query)
    return result.scalars().all()
    
# Функция для получения баланса конкретного пользователя
async def orm_get_user_balance(session: AsyncSession, user_id: int):
    query = select(User.balance).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar()

# Функция для обновления баланса пользователя
async def orm_update_users_balance(session: AsyncSession, current_balance: int, user_id: int):
    
    query = update(User).where(User.id == user_id).values(
        balance = current_balance
    )
    await session.execute(query)
    await session.commit()
    
# Функция для добавления действия пользователя в БД
async def orm_add_action_with_top_up(session: AsyncSession, user_id: int, user_name: str, action: str, top_up_amount: int):
    try:
        new_action = UserBalanceAction(
            user_id=user_id,
            user_name=user_name,
            action=action,
            top_up_balance_amount=top_up_amount
        )
        session.add(new_action)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка при добавлении действия пользователя: {e}")
        
# Функция для добавления идей пользвателю
async def orm_add_action_with_ideas(session: AsyncSession, user_id: int, chat_id:int,user_name: str, idea: str, for_who: int):
    try:
        new_action = Ideas(
            user_id=user_id,
            user_name=user_name,
            chat_id=chat_id,
            idea=idea,
            for_who=for_who
        )
        session.add(new_action)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка при добавлении идей пользователя: {e}")
        
# Функция для добавления идей пользвателю
async def orm_add_action_with_question(session: AsyncSession, user_id: int,chat_id:int, message_id:int, user_name: str, question: str, for_who: int):
    try:
        new_action = Questions(
            user_id=user_id,
            message_id=message_id,
            user_name=user_name,
            chat_id=chat_id, 
            question=question,
            for_who=for_who
        )
        session.add(new_action)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка при добавлении вопроса пользователя: {e}")


# Функция для получения вопроса конкретнокго пользователя
async def orm_get_user_question(session: AsyncSession, message_id: int):
    query = select(Questions.chat_id, Questions.question).where(Questions.message_id == message_id)
    result = await session.execute(query)
    return result.one_or_none()

# удаляем вопрос на который ответили из бд
async def orm_delete_user_question(session: AsyncSession, message_id: int):
    try:
        query = delete(Questions).where(Questions.message_id == message_id)
        await session.execute(query)
        await session.commit()
        print(f"Вопрос с message_id {message_id} был успешно удален.")
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка при удалении вопроса: {e}")
        
        
# Функция для получения вопроса имя пользователя и id сообщения
async def orm_get_all_questions(session: AsyncSession, for_who: str):
    query = select(Questions.user_name, Questions.message_id, Questions.question).where(Questions.for_who==for_who)
    result = await session.execute(query)
    return result.all()

# Функция для получения идеи имя пользователя и id сообщения
async def orm_get_all_ideas(session: AsyncSession, for_who: str):
    query = select(Ideas.user_name,Ideas.idea).where(Ideas.for_who==for_who)
    result = await session.execute(query)
    return result.all()