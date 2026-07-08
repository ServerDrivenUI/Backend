from .base_creator import BaseCreator
import json
from typing import Any, Dict, List, Tuple
from ..repository import ui_repo
from app.shared.consts import Icons
from beanie import PydanticObjectId
from typing import Optional


class NavbarCreator(BaseCreator):
    item_type: str = "navbar"

    _LOGOUT: str = "Выйти"
    _LOGIN: str = "Войти"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        navbar_doc = await ui_repo.get_element_by_type(self.item_type)
        if not navbar_doc:
            print("Элемент 'navbar' не найден в базе данных!")

        navbar_template = json.loads(navbar_doc.json_dict)

        nav_title_var = f"nav_title"
        nav_btn_var = f"nav_btn_text"

        nav_title = context.get("title") if context else "Default Title"

        for item in navbar_template.get("items", []):
            if item.get("id") == "navbar_title_layer":
                item["text"] = f"@{{nav_title}}"
            elif item.get("id") == "navbar_button_layer":
                item["text"] = f"@{{nav_btn_text}}"
            elif item.get("id") == "navbar_home_button":
                item["image_url"] = f"@{{home_icon}}"
            elif item.get("id") == "navbar_cart_button":
                item["image_url"] = f"@{{cart_icon}}"

        variables = []

        btn_title = self._LOGIN
        if user_id:
            btn_title = self._LOGOUT

        variables.append({"name": nav_title_var, "type": "string", "value": nav_title})
        variables.append({"name": nav_btn_var, "type": "string", "value": btn_title})
        variables.append(
            {
                "name": "home_icon",
                "type": "string",
                "value": Icons.HOME,
            }
        )
        variables.append(
            {
                "name": "cart_icon",
                "type": "string",
                "value": Icons.CART,
            }
        )

        return navbar_template, variables
