from app.shared.dbmodels import UIElement, ClothesItem, Page, Cart
from beanie import PydanticObjectId


class ContentRepository:
    """Работает с БД самого магазина"""

    async def get_all_clothes(self) -> list[ClothesItem]:
        clothes = await ClothesItem.find_all().to_list()
        return clothes

    async def get_user_cart(self, user_id: PydanticObjectId) -> list[ClothesItem]:
        cart_items = await Cart.find(Cart.user.id == user_id).all()

        clothes_items = []
        for cart in cart_items:
            clothes_items.append(cart.clothes)

        return clothes_items

    async def is_in_user_cart(
        self, user_id: PydanticObjectId, clothes_item_id: PydanticObjectId
    ) -> bool:
        cart = await Cart.find_one(
            Cart.user.id == user_id, Cart.clothes.id == clothes_item_id
        )
        return cart is not None


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
