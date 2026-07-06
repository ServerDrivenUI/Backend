from beanie import PydanticObjectId
import jwt
import os
from dotenv import load_dotenv
from fastapi import Depends, Request
from typing import Optional
from fastapi.security import HTTPAuthorizationCredentials
from app.shared.extensions import security
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

load_dotenv()


def get_id_from_token(self, token: str) -> PydanticObjectId | None:
    """Декодирует токен и возвращает PydanticObjectId вместо int"""
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=["HS256"],
        )
        return PydanticObjectId(payload["sub"])
    except Exception as e:
        self.logger.error(f"Ошибка токена {str(e)}")
        return None


async def get_current_user_id_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> PydanticObjectId:
    """Обязательный роут: использует стандартный security"""
    try:
        return get_id_from_token(None, credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


async def get_current_user_id_optional(request: Request) -> Optional[PydanticObjectId]:
    """Необязательный роут: читает заголовок напрямую из Request.
    FastAPI вообще не трогает этот запрос, если токена нет."""

    # 1. Извлекаем заголовок Authorization вручную
    auth_header = request.headers.get("Authorization")

    # Если заголовка нет — пользователь 100% гость, возвращаем None
    if not auth_header:
        return None

    # 2. Парсим строку "Bearer <token>"
    try:
        token_type, token = auth_header.split(" ", 1)
        if token_type.lower() != "bearer" or not token:
            return None  # Или raise HTTPException, если формат неверный
    except ValueError:
        return None

    # 3. Валидируем токен, если он был передан
    try:
        return get_id_from_token(None, token)
    except Exception:
        # Токен прислали, но он "битый" — выдаем ошибку
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
