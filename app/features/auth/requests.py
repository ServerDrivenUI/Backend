from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    """Запрос, содержащий данные для авторизации пользователя"""

    login: str = Field(
        ...,
        min_length=1,
        examples=["panfilovaakulina@example.com"],
        description="Логин пользователя",
    )
    """Логин пользователя"""

    password: str = Field(
        ..., min_length=1, examples=["76GTYXk8@K"], description="Пароль"
    )
    """Пароль"""
