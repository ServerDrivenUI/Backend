from fastapi import APIRouter

test_route = APIRouter(tags=["test"])

from . import route
