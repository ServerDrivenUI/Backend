import json
from typing import Dict, Any, List, Tuple, Optional
from beanie import PydanticObjectId
from .base_creator import BaseCreator
from app.core.repository import ui_repo


class BannerCreator(BaseCreator):
    item_type: str = "banner"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        context = context or {}

        hero_doc = await ui_repo.get_element_by_type(self.item_type)
        if not hero_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        hero_template = json.loads(hero_doc.json_dict)
        variables: List[Dict[str, Any]] = []

        hero_photo = context.get("hero_photo", "")
        hero_title = context.get("hero_title", "")
        hero_subtitle = context.get("hero_subtitle", "")

        if "background_image" in hero_template:
            hero_photo_var = "hero_photo"
            hero_template["background_image"]["url"] = f"@{{{hero_photo_var}}}"
            variables.append(
                {
                    "name": hero_photo_var,
                    "type": "string",
                    "value": hero_photo,
                }
            )

        for item in hero_template.get("items", []):
            if item.get("type") == "container":
                for sub_item in item.get("items", []):
                    if sub_item.get("id") == "hero_title":
                        hero_title_var = "hero_title"
                        sub_item["text"] = f"@{{{hero_title_var}}}"
                        variables.append(
                            {
                                "name": hero_title_var,
                                "type": "string",
                                "value": hero_title,
                            }
                        )

                    elif sub_item.get("id") == "hero_subtitle":
                        hero_subtitle_var = "hero_subtitle"
                        sub_item["text"] = f"@{{{hero_subtitle_var}}}"
                        variables.append(
                            {
                                "name": hero_subtitle_var,
                                "type": "string",
                                "value": hero_subtitle,
                            }
                        )

        return hero_template, variables
