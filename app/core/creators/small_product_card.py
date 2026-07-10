import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo


class SmallProductCardCreator(BaseCreator):
    item_type: str = "small_product_card"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        card_doc = await ui_repo.get_element_by_type(self.item_type)
        if not card_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        card_template = json.loads(card_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        product_img = context.get("product_img", "")
        product_name = context.get("product_name", "")
        product_description = context.get("product_description", "")
        price = context.get("product_price", "")
        product_id = str(context.get("id", "1"))

        item_id_var = f"item_id_{product_id}"
        item_id = context.get("clothes_item_id", product_id)

        variables.append(
            {
                "name": item_id_var,
                "type": "string",
                "value": item_id,
            }
        )

        def process_items(items: List[Dict[str, Any]]):
            for item in items:
                elem_id = item.get("id", "")

                if elem_id == "image":
                    img_var = f"product_img_{product_id}"
                    item["image_url"] = f"@{{{img_var}}}"
                    variables.append(
                        {"name": img_var, "type": "string", "value": product_img}
                    )

                elif elem_id == "name":
                    name_var = f"product_name_{product_id}"
                    item["text"] = f"@{{{name_var}}}"
                    variables.append(
                        {"name": name_var, "type": "string", "value": product_name}
                    )

                elif elem_id == "description":
                    desc_var = f"product_description_{product_id}"
                    item["text"] = f"@{{{desc_var}}}"
                    variables.append(
                        {
                            "name": desc_var,
                            "type": "string",
                            "value": product_description,
                        }
                    )

                elif elem_id == "price":
                    price_var = f"product_price_{product_id}"
                    item["text"] = f"@{{{price_var}}}"
                    variables.append(
                        {
                            "name": price_var,
                            "type": "string",
                            "value": f"{price:_} ₽".replace("_", " "),
                        }
                    )

                if "items" in item:
                    process_items(item["items"])

        if "action" in card_template and "url" in card_template["action"]:
            card_template["action"]["url"] = card_template["action"]["url"].replace(
                "@{item_id}", f"@{{{item_id_var}}}"
            )

        process_items(card_template.get("items", []))

        return card_template, variables
