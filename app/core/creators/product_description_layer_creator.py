from typing import Any, Dict, List, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
from beanie import PydanticObjectId
from typing import Optional
import json
from app.shared.consts import LOCAL_PHOTO


class ProductDescriptionCreator(BaseCreator):
    item_type: str = "product_description_layer"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        description_doc = await ui_repo.get_element_by_type(self.item_type)
        if not description_doc:
            raise(f"Элемент '{self.item_type}' не найден в базе данных!")

        description_template = json.loads(description_doc.json_dict)

        item_id = context.get("item_id")
        if not item_id:
            return description_template, []

        clothes = await content_repo.get_clothes_by_id(item_id)

        variables = [
            {
                "name": "product_description",
                "type": "string",
                "value": clothes.descripton,
            }
        ]

        return description_template, variables
