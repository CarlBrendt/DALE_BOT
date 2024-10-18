<<<<<<< HEAD
from aiogram.fsm.state import StatesGroup, State

class SupportState(StatesGroup):
    
    question_to_developer = State()
    idea_to_developer = State()
    question_to_seo = State()
    idea_to_seo = State()
    
    awaiting_response = State()
=======
from aiogram.fsm.state import StatesGroup, State

class SupportState(StatesGroup):
    
    question_to_developer = State()
    idea_to_developer = State()
    question_to_seo = State()
    idea_to_seo = State()
    
    awaiting_response = State()
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
    original_message_id = State()