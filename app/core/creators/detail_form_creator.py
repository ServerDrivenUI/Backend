from typing import Any, Dict, List, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
from beanie import PydanticObjectId
from typing import Optional
import json
from app.shared.consts import LOCAL_PHOTO


class DetailFormCreator(BaseCreator):
    item_type: str = "detail_form"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        detail_form_doc = await ui_repo.get_element_by_type(self.item_type)
        if not detail_form_doc:
            print(f"Элемент '{self.item_type}' не найден в базе данных!")
            return {}, []

        detail_template = json.loads(detail_form_doc.json_dict)

        items = []
        texts = detail_template["items"][1]["items"]
        for t in texts:
            text_doc = await ui_repo.get_element_by_type(t["type"])
            text_template = json.loads(text_doc.json_dict)
            items.append(text_template)

        detail_template["items"][1]["items"] = items

        item_id = context.get("clothes_item_id")

        clothes = await content_repo.get_clothes_by_id(item_id)

        variables = [
            {
                "name": "product_img",
                "type": "string",
                "value": LOCAL_PHOTO,
            },
            {"name": "product_title", "type": "string", "value": clothes.name},
            {"name": "product_price", "type": "string", "value": f"{clothes.price} ₽"},
            {
                "name": "product_description",
                "type": "string",
                "value": clothes.descripton,
            },
            {"name": "item_id", "type": "string", "value": str(clothes.id)},
        ]

        return detail_template, variables
