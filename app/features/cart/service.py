from .repository import cart_repo
from beanie import PydanticObjectId


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


cart_service = CartService()
