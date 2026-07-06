import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.shared.config import config_factory
from app.shared.extensions import (
    db,
    main_config,
)
from fastapi.staticfiles import StaticFiles

load_dotenv()

from contextlib import asynccontextmanager


def register_routes(app: FastAPI, routes: list):
    for r in routes:
        app.include_router(r)


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if hasattr(db, "init_app"):
            await db.init_app(app)

        if hasattr(config, "special_init_fastapi"):
            config.special_init_fastapi(app, db)

        yield

        if getattr(db, "client", None):
            db.client.close()

    app = FastAPI(title="Server Driven UI", lifespan=lifespan)

    app.mount("/assets", StaticFiles(directory="assets"), name="assets")
    print("Фото тестовое по http://localhost:5200/assets/clothes.jpg")
    print("Иконки http://localhost:5200/assets/basket-shopping-solid-full.svg")
    print("http://localhost:5200/assets/house-solid-full.svg")

    config_const = os.getenv("CONFIG")
    config = config_factory(config_const)

    app.state.config = config
    global main_config
    main_config = config

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from .shared import dbmodels
    from .features import routes

    register_routes(app, routes)

    return app
