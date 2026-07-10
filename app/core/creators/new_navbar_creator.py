import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.shared.consts import Icons
from app.core.repository import ui_repo


class NewNavbarCreator(BaseCreator):
    item_type: str = "new_navbar"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        navbar_doc = await ui_repo.get_element_by_type(self.item_type)
        if not navbar_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        navbar_template = json.loads(navbar_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        cart_count = context.get("cart_count", 0)

        for item in navbar_template.get("items", []):
            for sub_item in item.get("items", []):
                if sub_item.get("id") == "navbar_search_button":
                    sub_item["image_url"] = "@{search_icon}"
                    search_icon_var = "search_icon"
                    variables.append(
                        {
                            "name": search_icon_var,
                            "type": "string",
                            "value": Icons.SEARCH,
                        }
                    )

                elif sub_item.get("id") == "navbar_menu_button":
                    sub_item["image_url"] = "@{menu_icon}"
                    menu_icon_var = "menu_icon"
                    variables.append(
                        {
                            "name": menu_icon_var,
                            "type": "string",
                            "value": Icons.MENU,
                        }
                    )

                elif sub_item.get("type") == "container":
                    for cart_item in sub_item.get("items", []):
                        if cart_item.get("id") == "navbar_cart_icon":
                            cart_item["image_url"] = "@{cart_icon}"
                            cart_icon_var = "cart_icon"
                            variables.append(
                                {
                                    "name": cart_icon_var,
                                    "type": "string",
                                    "value": Icons.CART,
                                }
                            )

                        elif cart_item.get("id") == "navbar_cart_badge":
                            cart_count_var = "cart_count"
                            cart_item["text"] = f"@{{{cart_count_var}}}"
                            variables.append(
                                {
                                    "name": cart_count_var,
                                    "type": "string",
                                    "value": str(cart_count),
                                }
                            )

                            cart_count_visible_var = "cart_count_visible"
                            cart_item["visibility"] = f"@{{{cart_count_visible_var}}}"
                            variables.append(
                                {
                                    "name": cart_count_visible_var,
                                    "type": "string",
                                    "value": (
                                        "visible" if cart_count > 0 else "invisible"
                                    ),
                                }
                            )

        return navbar_template, variables
