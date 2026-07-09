from pydantic import BaseModel, Field
from typing import Optional
from beanie import PydanticObjectId


class PageRequest(BaseModel):
    """Запрос, содержащий тип страницы"""

    type: str = Field(
        ...,
        min_length=1,
        examples=["main_market_page"],
        description="Тип страницы в БД",
    )
    """Тип страницы"""

    clothes_item_id: Optional[PydanticObjectId] = Field(
        default=None,
        examples=["6a480f0c67d986ddd81b7a93"],
        description="Id товара",
    )
    """Id товара"""
