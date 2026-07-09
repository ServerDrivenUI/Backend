from typing import Any, Dict, List, Optional, Tuple
from app.core.repository import content_repo, ui_repo
from app.core.creators.base_creator import BaseCreator
from beanie import PydanticObjectId


class AuthCreator(BaseCreator):
    page_type: str = "auth_page"
    nav_title: str = "Авторизация"

    async def get_page(
        self,
        page_json: Dict[str, Any],
        user_id: Optional[PydanticObjectId] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        return page_json, []
