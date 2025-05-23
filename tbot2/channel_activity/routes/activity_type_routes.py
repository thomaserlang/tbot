from fastapi import APIRouter

from ..constants.activity_types_constants import ACTIVITY_TYPE_NAMES, ActivityTypeName

router = APIRouter()


@router.get('/activity-types', name='Activity Types')
async def get_activity_types_route() -> list[ActivityTypeName]:
    return ACTIVITY_TYPE_NAMES
