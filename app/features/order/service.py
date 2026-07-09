import logging
from beanie import PydanticObjectId
from .repository import order_repo


class OrderService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def create_order(self, user_id: PydanticObjectId):
        try:
            await order_repo.create_order_from_cart(user_id)
        except Exception as e:
            self.logger.error(f"Ошибка создания заказа из корзины: {str(e)}")
            raise Exception(f"Ошибка создания заказа из корзины: {str(e)}")

    async def create_one_order(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ):
        try:
            await order_repo.create_one_order(user_id, clothes_item_id)
        except Exception as e:
            self.logger.error(f"Ошибка создания заказа из 1 товара: {str(e)}")
            raise Exception(f"Ошибка создания заказа из 1 товара: {str(e)}")


order_service = OrderService()
