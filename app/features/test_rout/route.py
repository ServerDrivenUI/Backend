from . import test_route

@test_route.get("/test")
async def test_endpoint():
    return {"message": "Тестовый /test"}
