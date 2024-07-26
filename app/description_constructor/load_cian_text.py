import aiohttp
import asyncio
from config_reader import config

DIFFBOT_TOKEN = config.diffbot_token.get_secret_value()

async def fetch_data(session, url):
    
    """ 
    Отправляет асинхронный GET-запрос к указанному URL и возвращает JSON-ответ.
    Это универсальный метод для получения данных.
    """
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None  # or handle error

async def get_all_info_from_link(link):
    """
    Преобразует URL жк для использования в API Diffbot, отправляет запрос с помощью fetch_data,
    и обрабатывает полученные данные, пытаясь извлечь текст. 
    """
    
    link = link.split('/')[-2].split('.')[0]
    # Construct the URL for the API request
    api_url = f"https://api.diffbot.com/v3/article?url=https%3A%2F%2F{link}.cian.ru%2F&token={DIFFBOT_TOKEN}"
    
    # Create an aiohttp ClientSession
    async with aiohttp.ClientSession() as session:
        response_data = await fetch_data(session, api_url)
        
        # Check if the response data is not None and try to parse the text
        if response_data and 'objects' in response_data:
            try:
                text = response_data['objects'][-1]['text']
                return text
            except (IndexError, KeyError):
                return "No text found or error parsing the text."
        else:
            return "Failed to fetch or parse data."

# Asynchronous main function to run the async task
async def main():
    
    link = "https://zhk-eniteo-i.cian.ru/"
    text = await get_all_info_from_link(link)
    print(text)

if __name__ == "__main__":
    asyncio.run(main())