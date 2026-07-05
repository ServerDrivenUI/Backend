from app.shared.dbmodels import Cart, ClothesItem, User
from beanie import PydanticObjectId


class CartRepository:
    """Репозиторий для управления корзиной"""

    async def add(self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId):
        """Вставка документа корзины с проверкой на дубликаты"""
        
        existing_entry = await Cart.find_one(
            Cart.user.id == user_id,
            Cart.clothes.id == clothes_item_id
        )
        
        if existing_entry:
            return existing_entry
            
        cart_entry = Cart(
            user=User.link_from_id(user_id),
            clothes=ClothesItem.link_from_id(clothes_item_id)
        )
        
        await cart_entry.insert()
        return cart_entry

    async def remove(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ):
        """Поиск и удаление элемента корзины"""
        cart_entry = await Cart.find_one(
            Cart.user.id == user_id, Cart.clothes.id == clothes_item_id
        )
        if cart_entry:
            await cart_entry.delete()
            return True
        return False


cart_repo = CartRepository()
