from .response import PageResponse
from fastapi import APIRouter
from .service import pages_service
from .requests import PageRequest
from beanie import PydanticObjectId
from fastapi import Depends
from app.shared.token import get_current_user_id_optional
from typing import Optional

pages_route = APIRouter(tags=["pages"])


@pages_route.post("/pages")
async def page_endpoint(
    body: PageRequest,
    user_id: Optional[PydanticObjectId] = Depends(get_current_user_id_optional),
):
    try:
        result, background_color = await pages_service.get_page(
            page_type=body.type, user_id=user_id, clothes_item_id=body.clothes_item_id
        )
        return PageResponse[dict](data=result, color=background_color)
    except Exception as e:
        return PageResponse[None](error=f"{str(e)}")
