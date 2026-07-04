from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    """Запрос, содержащий данные для авторизации пользователя"""

    login: str = Field(
        ...,
        min_length=1,
        examples=["gobrien@example.net"],
        description="Логин пользователя",
    )
    """Логин пользователя"""

    password: str = Field(
        ..., min_length=1, examples=["5S&aL(wg+G"], description="Пароль"
    )
    """Пароль"""
