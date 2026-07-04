from app.shared.response import ApiResponse
from fastapi import APIRouter
from .requests import AuthRequest

auth_route = APIRouter(tags=["auth"])


@auth_route.post("/login")
async def page_endpoint(body: AuthRequest):
    return ApiResponse[str](data="jwt")
