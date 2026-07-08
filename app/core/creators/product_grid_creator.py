import json
from typing import Any, Dict, List, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
import copy
from app.shared.consts import LOCAL_PHOTO
from beanie import PydanticObjectId
from typing import Optional
from . import register_creator


@register_creator
class ProductGridCreator(BaseCreator):
    item_type: str = "product_grid"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        grid_doc = await ui_repo.get_element_by_type(self.item_type)
        grid_template = json.loads(grid_doc.json_dict)

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

            local_already_in_cart_btn_str = json.dumps(local_already_in_cart_btn)
            local_already_in_cart_btn_str = local_already_in_cart_btn_str.replace(
                "item_id_PLACEHOLDER", item_id_var
            )
            local_already_in_cart_btn = json.loads(local_already_in_cart_btn_str)

            if "action" in local_cart_btn:
                local_cart_btn["action"][
                    "url"
                ] = f"myapp://add_to_cart?clothes_item_id=@{{{item_id_var}}}"

            if "action" in local_already_in_cart_btn:
                local_already_in_cart_btn["action"][
                    "url"
                ] = f"myapp://remove_from_cart?clothes_item_id=@{{{item_id_var}}}"

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

        grid_template["items"] = cards_with_data

        return grid_template, variables
