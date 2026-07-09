from typing import Any, Dict, List, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
from beanie import PydanticObjectId
from typing import Optional
import json


class AuthCreator(BaseCreator):
    item_type: str = "auth_form"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        auth_form_doc = await ui_repo.get_element_by_type(self.item_type)
        if not auth_form_doc:
            raise Exception(f"Элемент {self.item_type} не найден в базе данных!")

        auth_template = json.loads(auth_form_doc.json_dict)

        return auth_template, []
