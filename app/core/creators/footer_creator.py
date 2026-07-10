import json
from typing import Dict, Any, Optional, List, Tuple
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo


class FooterCreator(BaseCreator):
    item_type: str = "footer"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Получает шаблон footer из БД и возвращает его с переменными"""
        footer_doc = await ui_repo.get_element_by_type(self.item_type)
        if not footer_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        footer_template = json.loads(footer_doc.json_dict)

        variables = []

        return footer_template, variables
