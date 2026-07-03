from app.shared.response import ApiResponse
from .service import test_service
from fastapi import APIRouter

test_route = APIRouter(tags=["test"])


@test_route.get("/test")
async def test_endpoint():
    test_service.test()
    return ApiResponse(data="Тестовый /test")
