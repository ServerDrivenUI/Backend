from .repository import cart_repo
from beanie import PydanticObjectId
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.shared.extensions import security
from app.shared.token import get_id_from_token


class CartService:
    """Сервис бизнес-логики корзины"""

    async def add_to_cart(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ):
        """Добавление в корзину через репозиторий"""
        return await cart_repo.add(user_id, clothes_item_id)

    async def remove_from_cart(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ):
        """Удаление из корзины через репозиторий"""
        return await cart_repo.remove(user_id, clothes_item_id)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> PydanticObjectId:
    return get_id_from_token(None, credentials.credentials)


cart_service = CartService()
