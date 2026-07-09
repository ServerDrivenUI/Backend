import json
from typing import Any, Dict, List, Optional, Tuple

from beanie import PydanticObjectId

from app.core.creators.base_creator import BaseCreator
from app.core.repository import ui_repo


class StaticCreator(BaseCreator):
    def __init__(self, type_name: str):
        self.item_type = type_name

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        is_impulsive = context.get("is_impulsive", False) if context else False

        doc = await ui_repo.get_element_by_type(self.item_type, is_impulsive)
        if not doc:
            return context or {}, []

        return json.loads(doc.json_dict), []
