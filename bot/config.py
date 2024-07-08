import os

from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    bot_token: str = os.getenv('BOT_TOKEN')

    mongo_host: str = os.getenv('MONGO_HOST')
    mongo_port: int = int(os.getenv('MONGO_PORT'))


settings = Settings()
