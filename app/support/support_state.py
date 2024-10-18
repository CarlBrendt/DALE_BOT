from aiogram.fsm.state import StatesGroup, State

class SupportState(StatesGroup):
    
    question_to_developer = State()
    idea_to_developer = State()
    question_to_seo = State()
    idea_to_seo = State()
    
    awaiting_response = State()
    original_message_id = State()