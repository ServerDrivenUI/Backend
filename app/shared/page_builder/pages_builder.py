from .repository import ui_repo, pages_repo
import json
from typing import Any, Dict, List, Tuple
from .pages_creators import creators, BaseCreator


class PagesBuilder:
    """Собирает нужные страницы по их типу"""

    async def build_page(
        self, page_type: str
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        page = await pages_repo.get_page_by_type(page_type)
        if not page:
            self.logger.error(
                f"Страница с типом '{page_type}' не найдена в базе данных"
            )
            return None

        page_json = json.loads(page.json_dict)

        creator = self._get_creator(page_type)

        page_json, variables = await creator.get_page(page_json)

        navbar_template = await self._add_navbar()

        final_screen = await self._add_background(page_json, navbar_template)

        return final_screen, variables

    async def _add_navbar(self) -> Dict[str, Any]:
        navbar_doc = await ui_repo.get_element_by_type("navbar")
        if not navbar_doc:
            raise ValueError("Элемент 'navbar' не найден в базе данных!")
        return json.loads(navbar_doc.json_dict)

    async def _add_background(
        self, page_json: Dict[str, Any], navbar_template: Dict[str, Any]
    ) -> Dict[str, Any]:
        background_doc = await ui_repo.get_element_by_type("background")
        if not background_doc:
            raise ValueError("Элемент 'background' не найден в базе данных!")
        background_template = json.loads(background_doc.json_dict)

        content_doc = await ui_repo.get_element_by_type("content")
        if not content_doc:
            raise ValueError("Элемент 'content' не найден в базе данных!")
        content_template = json.loads(content_doc.json_dict)

        content_template["items"].insert(1, page_json)

        background_template["items"].insert(0, navbar_template)
        background_template["items"].insert(1, content_template)

        return background_template

    def _get_creator(self, page_type: str) -> BaseCreator | None:
        """Определяет нужный создатель страницы"""
        for c in creators:
            if c.page_type == page_type:
                return c

        return None


page_builder = PagesBuilder()
