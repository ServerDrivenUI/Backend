from typing import Optional

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.shared.dbmodels import User, UserAction
from app.shared.response import ApiResponse
from app.shared.token import get_current_user_id_optional

track_route = APIRouter(tags=["track"])


class TrackRequest(BaseModel):
    action_type: str
    item_id: Optional[str] = None


async def recalculate_buyer_type(user_id: PydanticObjectId):
    actions = await UserAction.find({"user.$id": ObjectId(str(user_id))}).to_list()
    views = len([a for a in actions if a.action_type == "view_product"])
    purchases = len(
        [a for a in actions if a.action_type in ("buy", "add_to_cart")]
    )

    if purchases == 0:
        return

    user = await User.get(user_id)
    if not user:
        return

    user.is_impulsive = (views / purchases) < 2
    await user.save()


@track_route.post("/track")
async def track(
    body: TrackRequest,
    user_id: Optional[PydanticObjectId] = Depends(get_current_user_id_optional),
):
    if user_id:
        await UserAction(
            user=User.link_from_id(user_id),
            action_type=body.action_type,
            item_id=body.item_id,
        ).save()
        await recalculate_buyer_type(user_id)

    return ApiResponse[str](data="OK")
