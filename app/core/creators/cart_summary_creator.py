import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo, content_repo


class CartSummaryCreator(BaseCreator):
    item_type: str = "cart_summary"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        summary_doc = await ui_repo.get_element_by_type(self.item_type)
        if not summary_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        summary_template = json.loads(summary_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        cart_items = await content_repo.get_user_cart(user_id)
        s = 0
        for c in cart_items:
            s = s + c.price

        sum = f"{s:_} ₽".replace("_", " ")

        for item in summary_template.get("items", []):
            if item.get("type") == "container":
                for sub_item in item.get("items", []):
                    if sub_item.get("id") == "pre_sum":
                        pre_sum_var = "pre_sum"
                        sub_item["text"] = f"@{{{pre_sum_var}}}"
                        variables.append(
                            {
                                "name": pre_sum_var,
                                "type": "string",
                                "value": sum,
                            }
                        )
                    if sub_item.get("id") == "sum":
                        sum_var = "sum"
                        sub_item["text"] = f"@{{{sum_var}}}"
                        variables.append(
                            {
                                "name": sum_var,
                                "type": "string",
                                "value": sum,
                            }
                        )

        return summary_template, variables
