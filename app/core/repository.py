from app.shared.dbmodels import UIElement, ClothesItem, Page


class ContentRepository:
    """Работает с БД самого магазина"""

    async def get_all_clothes(self) -> list[ClothesItem]:
        clothes = await ClothesItem.find_all().to_list()
        return clothes


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
