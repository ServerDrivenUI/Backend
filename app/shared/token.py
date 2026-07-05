from beanie import PydanticObjectId
import jwt
import os
from dotenv import load_dotenv

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
