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

        page_json = await self._add_navbar(page_json)

        return page_json, variables

    async def _add_navbar(self, page_json: Dict[str, Any]) -> Dict[str, Any]:
        navbar_doc = await ui_repo.get_element_by_type("navbar")
        if not navbar_doc:
            raise ValueError("Элемент 'navbar' не найден в базе данных!")
        navbar_template = json.loads(navbar_doc.json_dict)

        page_json["items"].insert(0, navbar_template)

        return page_json

    def _get_creator(self, page_type: str) -> BaseCreator | None:
        """Определяет нужный создатель страницы"""
        for c in creators:
            if c.page_type == page_type:
                return c

        return None


page_builder = PagesBuilder()
