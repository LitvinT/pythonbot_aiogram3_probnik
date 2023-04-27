import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from telegraph.aio import Telegraph


BASE_DIR = Path(__file__).resolve().parent
load_dotenv()
bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    parse_mode='HTML'
)
DATABASE_URL = f'{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOST")}' \
               f':{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'
dp = Dispatcher()
telegraph = Telegraph(access_token='8d8a4fbdf6d86859957750e288c63d260a95ecba4106b0dd6b2eca566db5')
