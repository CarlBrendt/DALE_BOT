import openai
import os
from config_reader import config
import aiohttp
import asyncio
from openai import AsyncOpenAI

os.environ['OPENAI_API_KEY'] = config.openai_key.get_secret_value()

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

async def get_chatgpt_response(system_prompt, user_text):
    
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            max_tokens=4096,
            temperature=0.7,
        )
        return response.choices[0].message.content

async def main_gpt():
    prompt = input("Enter your prompt: ")
    response = await get_chatgpt_response(prompt, prompt)
    print("ChatGPT response:", response)

if __name__ == '__main__':
    asyncio.run(main_gpt())
