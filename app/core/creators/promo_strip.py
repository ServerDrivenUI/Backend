import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo


class PromoStripCreator(BaseCreator):
    item_type: str = "promo_strip"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        promo_doc = await ui_repo.get_element_by_type(self.item_type)
        if not promo_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        promo_template = json.loads(promo_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        promo_text = context.get("promo_text", "")

        for item in promo_template.get("items", []):
            if item.get("type") == "text":
                promo_text_var = "promo_text"
                item["text"] = f"@{{{promo_text_var}}}"
                variables.append(
                    {
                        "name": promo_text_var,
                        "type": "string",
                        "value": promo_text,
                    }
                )

        return promo_template, variables
