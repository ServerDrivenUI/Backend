from ..repository import ui_repo, pages_repo
import json
from typing import Any, Dict, List, Tuple
from beanie import PydanticObjectId
from typing import Optional
from .base_pages_builder import BasePagesBuilder
from app.shared.consts import DesignIds


class GreenPagesBuilder(BasePagesBuilder):
    """Собирает нужные страницы по их типу"""

    DESIGN_ID: str = DesignIds.GREEN

    def __init__(self, _creators):
        super().__init__(_creators)

    async def build_page(
        self, page_type: str, user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        page = await pages_repo.get_page_by_type(page_type)
        if not page:
            print(f"Страница с типом '{page_type}' не найдена в базе данных")
            return None

        page_json = json.loads(page.json_dict)

        creator = self._get_creator(page_type)

        page_json, variables = await creator.get_page(page_json, user_id)

        navbar_template, nav_bar_variabals = await self._add_navbar(
            creator.nav_title, creator.page_type, user_id
        )

        final_screen = await self._add_background(page_json, navbar_template)
        final_variables = variables + nav_bar_variabals

        return final_screen, final_variables

    async def _add_navbar(
        self, nav_title: str, page_type: str, user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        LOGOUT = "Выйти"
        LOGIN = "Войти"

        navbar_doc = await ui_repo.get_element_by_type("navbar")
        if not navbar_doc:
            print("Элемент 'navbar' не найден в базе данных!")

        navbar_template = json.loads(navbar_doc.json_dict)

        nav_title_var = f"nav_title_{page_type}"
        nav_btn_var = f"nav_btn_{page_type}"

        def update_navbar(elements_list):
            for item in elements_list:
                element_id = item.get("id")

                if element_id == "navbar_title_layer":
                    item["text"] = f"@{{{nav_title_var}}}"
                elif element_id == "navbar_button_layer":
                    item["text"] = f"@{{{nav_btn_var}}}"

                if "items" in item:
                    update_navbar(item["items"])

        if "items" in navbar_template:
            update_navbar(navbar_template["items"])

        variables = []

        btn_title = LOGIN
        if user_id:
            btn_title = LOGOUT

        variables.append({"name": nav_title_var, "type": "string", "value": nav_title})
        variables.append({"name": nav_btn_var, "type": "string", "value": btn_title})
        variables.append(
            {
                "name": "home_icon",
                "type": "string",
                "value": "http://localhost:5200/assets/house-solid-full.svg",
            }
        )
        variables.append(
            {
                "name": "cart_icon",
                "type": "string",
                "value": "http://localhost:5200/assets/basket-shopping-solid-full.svg",
            }
        )

        return navbar_template, variables

    async def _add_background(
        self, page_json: Dict[str, Any], navbar_template: Dict[str, Any]
    ) -> Dict[str, Any]:
        background_doc = await ui_repo.get_element_by_type("background")
        if not background_doc:
            raise ValueError("Элемент 'background' не найден в базе данных!")
        background_template = json.loads(background_doc.json_dict)

        content_doc = await ui_repo.get_element_by_type("content")
        if not content_doc:
            raise ValueError("Элемент 'content' не найден в базе данных!")
        content_template = json.loads(content_doc.json_dict)

        content_template["items"].insert(1, page_json)

        background_template["items"].insert(0, navbar_template)
        background_template["items"].insert(1, content_template)

        return background_template
