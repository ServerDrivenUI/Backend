from . import test_route
from app.shared.response import ApiResponse
from .service import test_service


@test_route.get("/test")
async def test_endpoint():
    return ApiResponse(data="Тестовый /test")
