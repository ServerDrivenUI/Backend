import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo, content_repo
from app.shared.consts import LOCAL_PHOTO
from .new_product_card_creator import ProductCardCreator


class ContentCreator(BaseCreator):
    item_type: str = "content"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        content_doc = await ui_repo.get_element_by_type(self.item_type)
        if not content_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        content_template = json.loads(content_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        elements = context.get("elements", "")

        if elements == "new_product_card":
            items, vars = await self._add_products()

            content_template["items"] = items
            variables = variables + vars

        return content_template, variables

    async def _add_products(self):
        creator: BaseCreator = ProductCardCreator()

        clothes = await content_repo.get_all_clothes()

        items = []
        variables = []

        for c in clothes:
            c_id = str(c.id)
            context = {
                "id": c_id,
                "product_img": LOCAL_PHOTO,
                "product_name": c.name,
                "product_description": c.descripton,
                "product_price": c.price,
            }

            try:
                item, vars = await creator.get_item(context)
                items.append(item)
                variables = variables + vars
            except Exception as e:
                raise Exception(
                    f"Ошибка создания элементов в {self.item_type}, элемент {c_id}"
                )

        return items, variables
