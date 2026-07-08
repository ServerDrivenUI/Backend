from beanie import PydanticObjectId
from app.shared.dbmodels import Cart, Order, OrderItem


class OrderRepository:
    async def create_order_from_cart(self, user_id: PydanticObjectId):
        cart_items = await Cart.find(Cart.user.id == user_id).to_list()

        if not cart_items:
            raise Exception("Корзина пуста")

        order = Order(user=user_id)
        await order.save()

        for cart_item in cart_items:
            order_item = OrderItem(order=order.id, clothes=cart_item.clothes)
            await order_item.save()

        await Cart.find(Cart.user.id == user_id).delete()

        return order


order_repo = OrderRepository()
