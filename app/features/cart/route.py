from app.shared.response import ApiResponse
from fastapi import APIRouter
from .service import cart_service
from app.shared.token import get_current_user_id_required
from .requests import CartRequest
from beanie import PydanticObjectId
from fastapi import Depends

cart_route = APIRouter(tags=["cart"])


@cart_route.post("/cart")
async def add_cart_endpoint(
    body: CartRequest,
    user_id: PydanticObjectId = Depends(get_current_user_id_required),
):
    result = await cart_service.add_to_cart(
        user_id=user_id, clothes_item_id=body.clothes_item_id
    )
    if result:
        return ApiResponse[str](data="OK")
    else:
        return ApiResponse[None](error="Ошибка добавления в корзину")


@cart_route.delete("/cart")
async def delete_cart_endpoint(
    body: CartRequest,
    user_id: PydanticObjectId = Depends(get_current_user_id_required),
):
    result = await cart_service.remove_from_cart(
        user_id=user_id, clothes_item_id=body.clothes_item_id
    )
    if result:
        return ApiResponse[str](data="OK")
    else:
        return ApiResponse[None](error="Ошибка удаления из корзины")
