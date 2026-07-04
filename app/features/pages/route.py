from app.shared.response import ApiResponse
from fastapi import APIRouter
from .service import pages_service
from .requests import PageRequest

pages_route = APIRouter(tags=["pages"])


@pages_route.post("/pages")
async def page_endpoint(body: PageRequest):
    result = await pages_service.get_page(body.type)
    return ApiResponse[dict](data=result)
