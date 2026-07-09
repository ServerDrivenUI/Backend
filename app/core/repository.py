from app.shared.dbmodels import UIElement, ClothesItem, Page, Cart
from beanie import PydanticObjectId
from bson import ObjectId


class ContentRepository:
    """Работает с БД самого магазина"""

    async def get_all_clothes(self) -> list[ClothesItem]:
        clothes = await ClothesItem.find_all().to_list()
        return clothes

    async def get_user_cart(self, user_id: PydanticObjectId) -> list[ClothesItem]:
        cart_items = await Cart.find({"user.$id": ObjectId(str(user_id))}).to_list()

        clothes_items = []
        for cart in cart_items:
            clothes_id = cart.clothes.to_ref().id
            item = await ClothesItem.get(clothes_id)
            if item:
                clothes_items.append(item)

        return clothes_items

    async def is_in_user_cart(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ) -> bool:
        cart = await Cart.find_one(
            Cart.user.id == user_id, Cart.clothes.id == clothes_item_id
        )
        return cart is not None

    async def get_clothes_by_id(self, item_id: PydanticObjectId) -> ClothesItem | None:
        return await ClothesItem.get(item_id)


class UIElementsRepository:
    """Работает с нужными шаблонами элементов UI"""

    async def get_element_by_type(self, type: str) -> UIElement:
        element = await UIElement.find_one(UIElement.type == type)
        return element


class PagesRepository:
    """Работает с шаблонами страниц"""

    async def get_page_by_type(self, type: str) -> Page | None:
        page = await Page.find_one(Page.type == type)
        return page


pages_repo = PagesRepository()
content_repo = ContentRepository()
ui_repo = UIElementsRepository()
