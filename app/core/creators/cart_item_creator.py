import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo


class CartItemCreator(BaseCreator):
    item_type: str = "new_cart_item"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        item_doc = await ui_repo.get_element_by_type(self.item_type)
        if not item_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        item_template = json.loads(item_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        cart_image = context.get("cart_image", "")
        name = context.get("name", "")
        description = context.get("description", "")
        price = context.get("price", "")
        product_id = str(context.get("id", "1"))

        def process_items(items: List[Dict[str, Any]]):
            for item in items:
                item_id = item.get("id", "")

                if item_id == "cart_image":
                    img_var = f"cart_image_{product_id}"
                    item["image_url"] = f"@{{{img_var}}}"
                    variables.append({
                        "name": img_var,
                        "type": "string",
                        "value": cart_image,
                    })

                elif item_id == "name":
                    name_var = f"cart_name_{product_id}"
                    item["text"] = f"@{{{name_var}}}"
                    variables.append({
                        "name": name_var,
                        "type": "string",
                        "value": name,
                    })

                elif item_id == "description":
                    desc_var = f"cart_description_{product_id}"
                    item["text"] = f"@{{{desc_var}}}"
                    variables.append({
                        "name": desc_var,
                        "type": "string",
                        "value": description,
                    })

                elif item_id == "cart_price":
                    price_var = f"cart_price_{product_id}"
                    item["text"] = f"@{{{price_var}}}"
                    variables.append({
                        "name": price_var,
                        "type": "string",
                        "value": price,
                    })

                if "items" in item:
                    process_items(item["items"])

        process_items(item_template.get("items", []))

        return item_template, variables