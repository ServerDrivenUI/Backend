import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo, content_repo
from app.shared.consts import LOCAL_PHOTO


class ProductCardCreator(BaseCreator):
    item_type: str = "new_product_card"

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

        clothes_id = context.get("clothes_item_id")
        clothes = await content_repo.get_clothes_by_id(clothes_id)

        product_img = LOCAL_PHOTO
        product_name = clothes.name
        product_description = clothes.descripton
        price = clothes.price
        old_price = clothes.price
        product_id = context.get("id", "1")

        item_id_var = f"item_id_{product_id}"
        variables.append(
            {
                "name": item_id_var,
                "type": "string",
                "value": str(clothes_id),
            }
        )

        def process_items(items: List[Dict[str, Any]]):
            for item in items:
                item_id = item.get("id", "")

                if item_id == "img":
                    img_var = f"product_img_{product_id}"
                    item["image_url"] = f"@{{{img_var}}}"
                    variables.append(
                        {
                            "name": img_var,
                            "type": "string",
                            "value": product_img,
                        }
                    )

                elif item_id == "name":
                    name_var = f"product_name_{product_id}"
                    item["text"] = f"@{{{name_var}}}"
                    variables.append(
                        {
                            "name": name_var,
                            "type": "string",
                            "value": product_name,
                        }
                    )

                elif item_id == "price":
                    if item.get("font_size") == 22:
                        price_var = f"product_price_{product_id}"
                        item["text"] = f"@{{{price_var}}}"
                        variables.append(
                            {
                                "name": price_var,
                                "type": "string",
                                "value": price,
                            }
                        )
                    elif item.get("strike") == "single":
                        old_price_var = f"product_old_price_{product_id}"
                        item["text"] = f"@{{{old_price_var}}}"
                        variables.append(
                            {
                                "name": old_price_var,
                                "type": "string",
                                "value": old_price,
                            }
                        )

                elif item_id == "description":
                    desc_var = f"product_description_{product_id}"
                    item["text"] = f"@{{{desc_var}}}"
                    variables.append(
                        {
                            "name": desc_var,
                            "type": "string",
                            "value": product_description,
                        }
                    )

                variables.append(
                    {"type": "string", "name": "selected_size", "value": "M"}
                )
                variables.append({"type": "integer", "name": "quantity", "value": 1})

                if "action" in item and "url" in item["action"]:
                    item["action"]["url"] = item["action"]["url"].replace(
                        "@{item_id}", f"@{{{item_id_var}}}"
                    )

                if "items" in item:
                    process_items(item["items"])

        if "action" in card_template and "url" in card_template["action"]:
            card_template["action"]["url"] = card_template["action"]["url"].replace(
                "@{item_id}", f"@{{{item_id_var}}}"
            )

        process_items(card_template.get("items", []))

        variables.append({"type": "string", "name": "selected_size", "value": "M"})
        variables.append({"type": "integer", "name": "quantity", "value": 1})

        return card_template, variables
