from all_config import config
import asyncio
from app.description_constructor.gpt_usage import get_chatgpt_response # асинхронная функция получения ответа от gpt
from app.description_constructor.load_cian_text import get_all_info_from_link # асинхронная функция получения информации о жк с сайта циан
import re
    
SYSTEM_PROMPT_HOUSE = config.SYSTEM_PROMPT_FOR_HOUSE
SYSTEM_PROMPT_FOR_FLAT_DESCRIPTION = config.SYSTEM_PROMPT_FOR_FLAT

# уникалим текст о жк с циана для дальнейшего использования
async def create_unique_description_of_building(info_about_building, extra_info):
    
    # пользователь может передать как ссылку на жк
    # так и информацию введнную вручную, потому что на циане может не быть информации
    url_pattern = r'^https:\/\/[\w-]+\.cian\.ru\/$'
    if re.match(url_pattern, info_about_building):
        text = await get_all_info_from_link(info_about_building)
        text = f"{text} , ОБЯЗАТЕЛЬНО УЧЕСТЬ В ОПИСАНИИ{extra_info}"
    else:
        text = info_about_building
        text = f"{text} , ОБЯЗАТЕЛЬНО УЧЕСТЬ В ОПИСАНИИ{extra_info}"
        
    unique_text = await get_chatgpt_response(SYSTEM_PROMPT_HOUSE, text)
    return unique_text

async def create_description_of_flat(info_about_flat, jk_info):
    combined_info = f"{info_about_flat}\n\nИнформация о ЖК:\n{jk_info}"
    print(await get_chatgpt_response(SYSTEM_PROMPT_FOR_FLAT_DESCRIPTION, combined_info))
    flat_text = await get_chatgpt_response(SYSTEM_PROMPT_FOR_FLAT_DESCRIPTION, combined_info)
    return flat_text

if __name__ == "__main__":
    asyncio.run(create_unique_description_of_building('https://zhk-skyview-i.cian.ru/'))