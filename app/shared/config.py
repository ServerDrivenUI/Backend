import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from fastapi import FastAPI
from app.shared.consts import JWT_ACCESS_TOKEN_EXPIRES

load_dotenv()


class BaseConfig(BaseSettings):
    """
    Base configuration class managing core application environment settings.
    """

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URI", "mongodb://localhost:27017/my_database"
    )
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "3xvX3jfKiSOoFFGVcIM5Hkd9o")
    JWT_ACCESS_TOKEN_EXPIRES_DAYS: int = JWT_ACCESS_TOKEN_EXPIRES
    APP_NAME: str = os.getenv("APP_NAME", "SDCV API")
    CONFIG: str = "DEBUG"

    def special_init_fastapi(self, app: FastAPI, db):
        """
        Initializes core base application components for FastAPI.
        """
        app.state.jwt_secret_key = self.JWT_SECRET_KEY
        app.state.jwt_expires = timedelta(days=self.JWT_ACCESS_TOKEN_EXPIRES_DAYS)


class DebugConfig(BaseConfig):
    """
    Development configuration environment containing Swagger documentation and extended logging.
    """
    CONFIG: str = "DEBUG"

    def special_init_fastapi(self, app: FastAPI, db):
        """
        Sets up the application in debug mode, modifying Swagger schema and active logging structures.
        """
        super().special_init_fastapi(app, db)
        
        print("Swagger on localhost:5200/docs")

        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

        os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                RotatingFileHandler(
                    os.path.join(BASE_DIR, "logs", "logs.log"),
                    encoding="utf-8",
                    maxBytes=10_000_000,
                    backupCount=5,
                ),
                logging.StreamHandler(),
            ],
        )
        print("Logs on backend/logs/")


class ProductConfig(BaseConfig):
    """
    Production configuration environment optimized for stable system deployment.
    """
    CONFIG: str = "PRODUCT"

    def special_init_fastapi(self, app: FastAPI, db):
        pass


configs = [DebugConfig(), ProductConfig()]


def config_factory(config: str) -> BaseConfig:
    for c in configs:
        if config == c.CONFIG:
            return c
    return configs[0]
