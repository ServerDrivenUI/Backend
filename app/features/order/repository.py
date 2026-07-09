from beanie import PydanticObjectId
from app.shared.dbmodels import Cart, Order, OrderItem, ClothesItem


class OrderRepository:
    async def create_order_from_cart(self, user_id: PydanticObjectId) -> Order:
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

    async def create_one_order(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ) -> Order:
        item = await ClothesItem.get(clothes_item_id)

        if not item:
            raise Exception("Товара нет")

        order = Order(user=user_id)
        await order.save()

        order_item = OrderItem(order=order, clothes=item)
        await order_item.save()

        return order


order_repo = OrderRepository()
