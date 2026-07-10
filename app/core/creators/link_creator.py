import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo


class LinkCreator(BaseCreator):
    item_type: str = "link"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        button_doc = await ui_repo.get_element_by_type(self.item_type)
        if not button_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        button_template = json.loads(button_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        link = context.get("link", "")
        number = context.get("num", "1")

        link_var = f"link{number}"
        button_template["text"] = f"@{{{link_var}}}"
        variables.append(
            {
                "name": link_var,
                "type": "string",
                "value": link,
            }
        )

        return button_template, variables
