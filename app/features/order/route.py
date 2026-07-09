from app.shared.response import ApiResponse
from fastapi import APIRouter
from app.shared.token import get_current_user_id_required
from beanie import PydanticObjectId
from fastapi import Depends
from .service import order_service
from .requests import OrderRequest

order_route = APIRouter(tags=["order"])


@order_route.get("/order")
async def order_endpoint(
    user_id: PydanticObjectId = Depends(get_current_user_id_required),
):
    result = await order_service.create_order(user_id)
    if result:
        return ApiResponse(data="Сделан заказ")
    else:
        return ApiResponse(error="Произошла ошибка")


@order_route.post("/order/item")
async def order_item_endpoint(
    body: OrderRequest,
    user_id: PydanticObjectId = Depends(get_current_user_id_required),
):
    result = await order_service.create_one_order(user_id, body.clothes_item_id)
    if result:
        return ApiResponse(data="Сделан заказ")
    else:
        return ApiResponse(error="Произошла ошибка")
