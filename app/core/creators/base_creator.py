from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
from beanie import PydanticObjectId
from typing import Optional


class BaseCreator(ABC):
    """Создают нужный элемент UI"""

    item_type: str = ""

    @abstractmethod
    async def get_item(
        self,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[PydanticObjectId] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        pass
