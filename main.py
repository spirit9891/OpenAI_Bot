import logging
import os
from typing import List
from dotenv import load_dotenv
import aiogram
from aiogram import Bot, Dispatcher, executor, types
import openai

load_dotenv()

# Get OpenAI API key and temperature from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_engine = os.getenv("OPENAI_ENGINE", "text-davinci-003")
openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.5"))
openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
dp = Dispatcher(bot)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Handle start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я Telegram бот, использующий OpenAI API. Чем могу помочь?")

# Handle help command
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Доступные команды: /help, /start, /settings")

# Handle settings command
@dp.message_handler(commands=['settings'])
async def send_settings(message: types.Message):
    settings_text = f"""
Текущая модель: {openai_engine}
Текущая температура модели: {openai_temperature}
Текущее значение 'max_tokens': {openai_max_tokens}
    """

    await message.reply(settings_text)

# Function to split text into chunks of maximum token length
def chunk_text(text: str, max_tokens: int) -> List[str]:
    chunks = []
    while len(text) > max_tokens:
        split_index = text.rfind('.', 0, max_tokens)
        if split_index == -1:
            split_index = max_tokens
        chunks.append(text[:split_index])
        text = text[split_index+1:]
    chunks.append(text)
    return chunks

# Handle any other message
@dp.message_handler()
async def handle_message(message: types.Message):
    chunks = chunk_text(message.text, max_tokens=openai_max_tokens)
    response_text = ""
    for chunk in chunks:
        response = openai.Completion.create(engine=openai_engine, prompt=chunk, max_tokens=openai_max_tokens, temperature=openai_temperature)
        if response.choices:
            response_text += response.choices[0]['text']
        else:
            response_text += "Извините, я не понимаю."
    await message.reply(response_text)


if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)
