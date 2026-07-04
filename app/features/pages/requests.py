from pydantic import BaseModel, Field


class PageRequest(BaseModel):
    """Запрос, содержащий тип страницы"""

    type: str = Field(
        ...,
        min_length=1,
        examples=["main_market_page"],
        description="Тип страницы в БД",
    )
    """Тип страницы"""
