from typing import Any, Dict, List, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
from beanie import PydanticObjectId
from typing import Optional


class AuthCreator(BaseCreator):
    page_type: str = "auth_page"
    nav_title: str = "Авторизация"

    async def get_item(
        self, page_json: Dict[str, Any], user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        return page_json, []
