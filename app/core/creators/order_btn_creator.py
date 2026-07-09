import json
from typing import Any, Dict, List, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
import copy
from app.shared.consts import LOCAL_PHOTO
from beanie import PydanticObjectId
from typing import Optional


class OrderBtnCreator(BaseCreator):
    item_type: str = "order_btn"

    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        order_btn_doc = await ui_repo.get_element_by_type(self.item_type)
        order_btn_template = json.loads(order_btn_doc.json_dict)

        return order_btn_template, []
