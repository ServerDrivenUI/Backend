import logging
from beanie import PydanticObjectId
from .repository import order_repo


class OrderService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def create_order(self, user_id: PydanticObjectId) -> bool:
        try:
            await order_repo.create_order_from_cart(user_id)
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    async def create_one_order(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ) -> bool:
        try:
            await order_repo.create_one_order(user_id, clothes_item_id)
            return True
        except Exception as e:
            self.logger.error(e)
            return False


order_service = OrderService()
