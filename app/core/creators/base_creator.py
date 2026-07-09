from abc import ABC, abstractmethod
import json
from typing import Any, Dict, List, Tuple
from ..repository import content_repo, ui_repo
import copy
from app.shared.consts import GLOBAL_PHOTO, LOCAL_PHOTO
from beanie import PydanticObjectId
from typing import Optional


class BaseCreator(ABC):
    """Создают именно нужную страницу"""

    page_type: str = ""
    nav_title: str = ""

    @abstractmethod
    async def get_page(
        self,
        page_json: Dict[str, Any],
        user_id: Optional[PydanticObjectId] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        pass
