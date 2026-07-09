import json
from typing import Any, Dict, List, Optional, Tuple

from beanie import PydanticObjectId

from app.core.creators.base_creator import BaseCreator
from app.core.repository import ui_repo


class StaticCreator(BaseCreator):
    nav_title: str = ""

    def __init__(self, type_name: str):
        self.page_type = type_name
        self.item_type = type_name

    async def get_page(
        self,
        page_json: Dict[str, Any],
        user_id: Optional[PydanticObjectId] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        is_impulsive = False
        if context:
            is_impulsive = context.get("is_impulsive", False)

        doc = await ui_repo.get_element_by_type(self.item_type, is_impulsive)
        if not doc:
            return page_json, []

        return json.loads(doc.json_dict), []
