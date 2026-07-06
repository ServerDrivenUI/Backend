from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi.security import HTTPBearer
from app.shared.config import BaseConfig
import os
from dotenv import load_dotenv

load_dotenv()

main_config: BaseConfig = None
security = HTTPBearer(auto_error=True)


class DatabaseExtension:

    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def init_app(self, app):
        global main_config
        db_uri = os.getenv("DATABASE_URI", "mongodb://localhost:27017/my_database")
        self.client = AsyncIOMotorClient(db_uri, serverSelectionTimeoutMS=3000)

        db_name = db_uri.split("/")[-1].split("?")[0] or "app_db"
        self.db = self.client[db_name]

        try:
            await self.client.admin.command("ping")
            print(f">>> [БД] Успешное подключение к MongoDB ({db_name})!")
        except Exception as e:
            print(f">>> [КРИТИЧЕСКАЯ ОШИБКА БД] Нет связи с MongoDB: {e}")

        from app.shared.dbmodels import get_beanie_models

        await init_beanie(
            database=self.db,
            document_models=get_beanie_models(),
        )


db = DatabaseExtension()
