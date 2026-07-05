import logging
from .repository import auth_repo
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv

load_dotenv()


class AuthService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def login(self, login: str, password: str) -> str | None:
        try:
            user = await auth_repo.get_user(login)
        except Exception as e:
            self.logger.error(f"Ошибка получения данных пользователя: {str(e)}")
            return None

        if not user:
            self.logger.warning("Пользователь не найден")
            return None

        is_equals = self.check_password(password, user.password_hash)
        if is_equals:
            user_id = user.id
            token = self._create_jwt_token(str(user_id))
            return token

        return None

    def check_password(self, password: str, password_hash: bytes) -> bool:
        """Проверяет совпадение пароля и его хэша"""
        # TODO: добавить хэш
        if password == password_hash:
            return True

        return False

    def _create_jwt_token(self, user_id: str) -> str:
        secret_key = os.getenv("JWT_SECRET_KEY")
        expire_time = datetime.now(timezone.utc) + timedelta(
            days=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
        )
        payload = {"sub": user_id, "exp": expire_time}
        return jwt.encode(payload, secret_key, algorithm="HS256")


auth_service = AuthService()
