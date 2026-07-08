from app.shared.response import ApiResponse
from fastapi import APIRouter
from app.shared.token import get_current_user_id_required
from beanie import PydanticObjectId
from fastapi import Depends

order_route = APIRouter(tags=["order"])


@order_route.get("/order")
async def order_endpoint(
    user_id: PydanticObjectId = Depends(get_current_user_id_required),
):
    return ApiResponse(data="Сделан заказ")
