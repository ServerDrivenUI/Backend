from app.shared.response import ApiResponse
from fastapi import APIRouter
from .service import genearate_service

generate_route = APIRouter(tags=["generate"])


@generate_route.get("/generate")
async def generate_endpoint():
    await genearate_service.generate_users(1)
    return ApiResponse(data="Генерация произошла")
