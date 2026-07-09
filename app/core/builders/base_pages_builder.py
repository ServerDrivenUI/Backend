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
            raise Exception(f"Страница с типом '{page_type}' не найдена в базе данных")

        page_json = json.loads(page.json_dict)

        templates = []
        variables = []

        items = page_json.get("items", [])
        for i in items:
            creator = self._get_creator(i["type"])
            i["clothes_item_id"] = clothes_item_id
            try:
                template, vars = await creator.get_item(i, user_id)
                templates.append(template)
                variables = variables + vars
            except Exception as e:
                raise Exception(f"Ошибка страницы {page_type}: {str(e)}")

        page_json["items"] = templates

        return page_json, variables

    def _get_creator(self, item_type: str) -> BaseCreator | None:
        """Определяет нужный создатель элемента"""

        return CREATORS_DICT.get(item_type)
