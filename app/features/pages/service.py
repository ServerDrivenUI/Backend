import logging
from app.core import page_builder
from app.shared.consts import SDUI_TEMPLATES
from beanie import PydanticObjectId
from typing import Optional, Any


class PagesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def get_page(
        self,
        page_type: str,
        user_id: Optional[PydanticObjectId] = None,
        clothes_item_id: Optional[PydanticObjectId] = None,
    ) -> tuple[dict[str, Any], str]:
        """Выбирает нужную страницу по ее типу из БД"""
        try:
            page_with_data, values = await page_builder.build_page(
                page_type, user_id, clothes_item_id
            )
        except Exception as e:
            self.logger.error(f"Ошибка создания страницы: {str(e)}")
            raise Exception(f"Ошибка создания страницы: {str(e)}")

        final_response = {
            "card": {
                "log_id": f"screen_{page_type}",
                "states": [{"state_id": 0, "div": page_with_data}],
                "variables": values,
            },
            "templates": SDUI_TEMPLATES,
        }

        return final_response, page_builder.COLORS.WHITE


pages_service = PagesService()
