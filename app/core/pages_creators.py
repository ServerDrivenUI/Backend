from abc import ABC, abstractmethod
import json
from typing import Any, Dict, List, Tuple
from .repository import content_repo, ui_repo
import copy
from app.shared.consts import GLOBAL_PHOTO, LOCAL_PHOTO
from beanie import PydanticObjectId
from typing import Optional


class BaseCreator(ABC):
    """Создают именно нужную страницу"""

    page_type: str = ""
    nav_title: str = ""

    @abstractmethod
    async def get_page(
        self, page_json: Dict[str, Any], user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        pass


class MainCreator(BaseCreator):
    page_type: str = "main_market_page"
    nav_title: str = "Главная"

    async def get_page(
        self, page_json: Dict[str, Any], user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        element_doc = await ui_repo.get_element_by_type("product_card")
        card_template = json.loads(element_doc.json_dict)

        cart_btn_doc = await ui_repo.get_element_by_type("cart_button")
        buy_btn_doc = await ui_repo.get_element_by_type("buy_button")
        already_bought_doc = await ui_repo.get_element_by_type("already_in_cart")

        cart_btn_template = json.loads(cart_btn_doc.json_dict)
        buy_btn_template = json.loads(buy_btn_doc.json_dict)
        already_in_cart_template = json.loads(already_bought_doc.json_dict)

        title_doc = await ui_repo.get_element_by_type("product_title_layer")
        price_doc = await ui_repo.get_element_by_type("product_price_layer")
        description_doc = await ui_repo.get_element_by_type("product_description_layer")

        title_template = json.loads(title_doc.json_dict)
        price_template = json.loads(price_doc.json_dict)
        description_template = json.loads(description_doc.json_dict)

        cards_with_data = []
        variables = []

        clothes = await content_repo.get_all_clothes()

        for c in clothes:
            c_id = str(c.id)
            local_card = copy.deepcopy(card_template)

            title_var = f"prod_title_{c_id}"
            price_var = f"prod_price_{c_id}"
            image_var = f"prod_img_{c_id}"
            description_var = f"prod_description_{c_id}"
            item_id_var = f"item_id_{c_id}"

            local_card["items"][1:1] = [
                copy.deepcopy(price_template),
                copy.deepcopy(title_template),
                copy.deepcopy(description_template),
            ]

            local_cart_btn = copy.deepcopy(cart_btn_template)
            local_already_in_cart_btn = copy.deepcopy(already_in_cart_template)
            local_buy_btn = copy.deepcopy(buy_btn_template)

            if "action" in local_cart_btn:
                local_cart_btn["action"][
                    "url"
                ] = f"myapp://add_to_cart?clothes_item_id=@{{{item_id_var}}}"

            if "action" in local_buy_btn:
                local_buy_btn["action"][
                    "url"
                ] = f"myapp://buy?clothes_item_id=@{{{item_id_var}}}"

            for item in local_card["items"]:
                element_id = item.get("id")

                if element_id == "product_badge_price_layer":
                    item["text"] = f"@{{{price_var}}}"

                elif element_id == "product_image_layer":
                    item["image_url"] = f"@{{{image_var}}}"

                elif element_id == "product_title_layer":
                    item["text"] = f"@{{{title_var}}}"

                elif element_id == "product_description_layer":
                    item["text"] = f"@{{{description_var}}}"

                elif element_id == "product_buttons_container":
                    if user_id and await content_repo.is_in_user_cart(user_id, c.id):
                        item["items"] = [
                            local_already_in_cart_btn,
                            local_buy_btn,
                        ]
                    else:
                        item["items"] = [
                            local_cart_btn,
                            local_buy_btn,
                        ]

            cards_with_data.append(local_card)

            variables.append({"name": title_var, "type": "string", "value": c.name})
            variables.append(
                {"name": price_var, "type": "string", "value": f"{c.price} ₽"}
            )
            variables.append(
                {"name": image_var, "type": "string", "value": LOCAL_PHOTO}
            )
            variables.append(
                {"name": description_var, "type": "string", "value": c.descripton}
            )
            variables.append({"name": item_id_var, "type": "string", "value": c_id})

        grid_found = False
        for item in page_json["items"]:
            if item.get("id") == "products_grid":
                item["items"] = cards_with_data
                grid_found = True
                break

        if not grid_found:
            raise ValueError(
                "Сетка с id='products_grid' не найдена в шаблоне страницы!"
            )

        return page_json, variables


class AuthCreator(BaseCreator):
    page_type: str = "auth_page"
    nav_title: str = "Авторизация"

    async def get_page(
        self, page_json: Dict[str, Any], user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        return page_json, []


class CartCreator(BaseCreator):
    page_type: str = "cart_page"
    nav_title: str = "Корзина"

    async def get_page(
        self, page_json: Dict[str, Any], user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        element_doc = await ui_repo.get_element_by_type("cart_element")
        cart_template = json.loads(element_doc.json_dict)

        title_doc = await ui_repo.get_element_by_type("product_title_layer")
        price_doc = await ui_repo.get_element_by_type("product_price_layer")
        description_doc = await ui_repo.get_element_by_type("product_description_layer")

        title_template = json.loads(title_doc.json_dict)
        price_template = json.loads(price_doc.json_dict)
        description_template = json.loads(description_doc.json_dict)

        cards_with_data = []
        variables = []

        clothes = await content_repo.get_all_clothes()

        for c in clothes:
            c_id = str(c.id)
            local_card = copy.deepcopy(cart_template)

            for item in local_card["items"]:
                if item.get("id") == "empty_text_container":
                    item["items"][0:0] = [
                        copy.deepcopy(price_template),
                        copy.deepcopy(title_template),
                        copy.deepcopy(description_template),
                    ]

            title_var = f"cart_title_{c_id}"
            price_var = f"cart_price_{c_id}"
            image_var = f"cart_img_{c_id}"
            description_var = f"cart_description_{c_id}"

            def update_elements(elements_list):
                for item in elements_list:
                    element_id = item.get("id")

                    if element_id == "product_title_layer":
                        item["text"] = f"@{{{title_var}}}"
                    elif element_id == "empty_image_layer":
                        item["image_url"] = f"@{{{image_var}}}"
                    elif element_id == "product_badge_price_layer":
                        item["text"] = f"@{{{price_var}}}"
                    elif element_id == "product_description_layer":
                        item["text"] = f"@{{{description_var}}}"

                    if "items" in item:
                        update_elements(item["items"])

            if "items" in local_card:
                update_elements(local_card["items"])

            cards_with_data.append(local_card)

            variables.append({"name": title_var, "type": "string", "value": c.name})
            variables.append(
                {"name": price_var, "type": "string", "value": f"{c.price} ₽"}
            )
            variables.append(
                {"name": image_var, "type": "string", "value": LOCAL_PHOTO}
            )
            variables.append(
                {
                    "name": description_var,
                    "type": "string",
                    "value": c.descripton,
                }
            )

        grid_found = False
        for item in page_json["items"]:
            if item.get("id") == "product_info_container":
                item["items"] = cards_with_data
                grid_found = True
                break

        if not grid_found:
            raise ValueError(
                "Сетка с id='product_info_container' не найдена в шаблоне страницы!"
            )

        return page_json, variables


creators = [MainCreator(), AuthCreator(), CartCreator()]
