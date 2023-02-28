import logging
import os

from dotenv import load_dotenv
import aiogram
from aiogram import Bot, Dispatcher, types, executor
import openai

load_dotenv()

# Get OpenAI API key and temperature from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_engine = os.getenv("OPENAI_ENGINE")
openai_temperature = float(os.getenv("OPENAI_TEMPERATURE"))
openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS"))

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
    await message.reply(f"Текущая температура модели OpenAI API: {openai_temperature}")

# Handle any other message
@dp.message_handler()
async def handle_message(message: types.Message):
    prompt = message.text
    response = openai.Completion.create(engine=openai_engine, prompt=prompt, max_tokens=openai_max_tokens, temperature=openai_temperature)

    if response.choices:
        await message.reply(response.choices[0]['text'])
    else:
        await message.reply("Извините, я не понимаю.")

if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)
