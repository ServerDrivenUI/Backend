from app.shared.response import ApiResponse
from fastapi import APIRouter
from .requests import AuthRequest
from .service import auth_service

auth_route = APIRouter(tags=["auth"])


@auth_route.post("/login")
async def page_endpoint(body: AuthRequest):
    jwt = await auth_service.login(body.login, body.password)
    return ApiResponse[str | None](data=jwt)
