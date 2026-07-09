from ..repository import ui_repo, pages_repo
import json
from typing import Any, Dict, List, Tuple
from beanie import PydanticObjectId
from typing import Optional
from dataclasses import dataclass
from app.core.creators.base_creator import BaseCreator
from app.core.creators import CREATORS_DICT


@dataclass(frozen=True)
class BaseColors:
    PRIMARY: str
    DARK: str
    WHITE: str
    BLACK: str
    BLACK_TEXT_1: str
    BLACK_TEXT_2: str


class BasePagesBuilder:
    """Собирает нужные страницы по их типу"""

    COLORS = BaseColors(
        PRIMARY="#42b077",
        DARK="#018a51",
        WHITE="#f0fff0",
        BLACK="#121212",
        BLACK_TEXT_1="#e6121212",
        BLACK_TEXT_2="#b3121212",
    )

    async def build_page(
        self,
        page_type: str,
        user_id: Optional[PydanticObjectId] = None,
        clothes_item_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        page = await pages_repo.get_page_by_type(page_type)
        if not page:
            print(f"Страница с типом '{page_type}' не найдена в базе данных")
            return None

        page_json = json.loads(page.json_dict)

        templates = []
        variables = []

        items = page_json.get("items", [])
        for i in items:
            creator = self._get_creator(i["type"])
            i["clothes_item_id"] = clothes_item_id
            template, vars = await creator.get_item(i, user_id)

            templates.append(template)
            variables = variables + vars

        page_json["items"] = templates

        return page_json, variables

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

    def _get_creator(self, item_type: str) -> BaseCreator | None:
        """Определяет нужный создатель элемента"""

        return CREATORS_DICT.get(item_type)
