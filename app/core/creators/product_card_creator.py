import json
from typing import Dict, Any, Optional, List, Tuple
from beanie import PydanticObjectId
from app.core.repository import ui_repo
from .base_creator import BaseCreator


class ProductCardCreator(BaseCreator):
    """Creator для карточки товара"""
    item_type: str = "product_card"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Получает шаблон product_card из БД, заменяет плейсхолдеры на имена переменных
        и возвращает шаблон + список переменных для PageBuilder
        """
        product_doc = await ui_repo.get_element_by_type(self.item_type)
        if not product_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        product_template = json.loads(product_doc.json_dict)
        variables = []

        if "action" in product_template and "url" in product_template["action"]:
            product_template["action"]["url"] = product_template["action"][
                "url"
            ].replace("@{product_id_PLACEHOLDER}", "@{product_id}")

        for item in product_template.get("items", []):
            if item.get("id") == "product_image_layer":
                item["image_url"] = "@{product_photo}"
                variables.append(
                    {
                        "name": "product_photo",
                        "type": "string",
                        "value": "",
                    }
                )

            elif item.get("type") == "text":
                if item.get("text") == "@{product_category}":
                    variables.append(
                        {"name": "product_category", "type": "string", "value": ""}
                    )
                elif item.get("text") == "@{product_name}":
                    variables.append(
                        {"name": "product_name", "type": "string", "value": ""}
                    )
                elif item.get("text") == "@{product_price_label}":
                    variables.append(
                        {"name": "product_price_label", "type": "string", "value": ""}
                    )
                elif item.get("text") == "@{product_compare_at_label}":
                    item["text"] = "@{product_compare_at_label}"
                    variables.append(
                        {
                            "name": "product_compare_at_label",
                            "type": "string",
                            "value": "",
                        }
                    )
                    variables.append(
                        {
                            "name": "product_has_discount",
                            "type": "boolean",
                            "value": False,
                        }
                    )

        variables.append({"name": "product_id", "type": "string", "value": ""})

        return product_template, variables
