from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class CartRequest(BaseModel):
    """Запрос для работы с корзиной"""

    clothes_item_id: PydanticObjectId = Field(
        ...,
        examples=["6a480f0c67d986ddd81b7a93"],
        description="Id товара",
    )
    """Id товара"""
