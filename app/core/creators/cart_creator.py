import json
from typing import Any, Dict, List, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
import copy
from app.shared.consts import LOCAL_PHOTO
from beanie import PydanticObjectId
from typing import Optional


class CartCreator(BaseCreator):
    page_type: str = "cart_page"
    nav_title: str = "Корзина"

    async def get_item(
        self, page_json: Dict[str, Any], user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        if not user_id:
            raise Exception("Не Авторизован, нет jwt токена")

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

        clothes = await content_repo.get_user_cart(user_id)

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
            item_id_var = f"item_id_{c_id}"

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
                    elif element_id == "empty_close_button":
                        if "action" in item and "url" in item["action"]:
                            item["action"][
                                "url"
                            ] = f"myapp://remove_from_cart?clothes_item_id=@{{{item_id_var}}}"

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
            variables.append({"name": item_id_var, "type": "string", "value": c_id})

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
