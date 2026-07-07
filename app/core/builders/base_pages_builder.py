from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
from app.core.creators.base_creator import BaseCreator
from beanie import PydanticObjectId
from typing import Optional


class BasePagesBuilder(ABC):
    """Собирает нужные страницы по их типу"""

    creators: list[BaseCreator]
    DESIGN_ID: str = ""

    def __init__(self, _creators: list[BaseCreator]):
        self.creators = _creators

    @abstractmethod
    async def build_page(
        self, page_type: str, user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        pass

    @abstractmethod
    async def _add_navbar(
        self, nav_title: str, page_type: str, user_id: Optional[PydanticObjectId] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        pass

    @abstractmethod
    async def _add_background(
        self, page_json: Dict[str, Any], navbar_template: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    def _get_creator(self, page_type: str) -> BaseCreator | None:
        """Определяет нужный создатель страницы"""
        for c in self.creators:
            if c.page_type == page_type:
                return c

        return None
