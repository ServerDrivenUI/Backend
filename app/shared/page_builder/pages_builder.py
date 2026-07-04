from .repository import content_repo, ui_repo
import json
import copy
from app.shared.consts import GLOBAL_PHOTO, LOCAL_PHOTO


class PagesBuilder:
    """Собирает нужные страницы по их типу"""

    async def build_main_market_page(self, page_json):
        navbar_doc = await ui_repo.get_element_by_type("navbar")
        if not navbar_doc:
            raise ValueError("Элемент 'navbar' не найден в базе данных!")
        navbar_template = json.loads(navbar_doc.json_dict)

        element_doc = await ui_repo.get_element_by_type("product_card")
        card_template = json.loads(element_doc.json_dict)

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

            cards_with_data.append(local_card)

            variables.append({"name": title_var, "type": "string", "value": c.name})
            variables.append(
                {"name": price_var, "type": "string", "value": f"{c.price} ₽"}
            )
            variables.append(
                {"name": image_var, "type": "string", "value": GLOBAL_PHOTO}
            )
            variables.append(
                {"name": description_var, "type": "string", "value": c.descripton}
            )

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

        page_json["items"].insert(0, navbar_template)

        return page_json, variables


page_builder = PagesBuilder()
