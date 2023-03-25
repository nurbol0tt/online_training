from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.exc import DatabaseError
from starlette import status

from app.dto.application import ProfileSchema
from app.dto.profile import (
    CreateProfileRequest,
    CreateProfileResponse,
    UpdateProfileResponse,
    UpdateProfileRequest
)
from app.dto.user import CurrentUser
from app.service.profile import (
    CreateProfile,
    ReadTeacher, UpdateProfile
)
from app.utils.auth.oauth2 import (
    get_current_user,
    get_current_user2
)

router = APIRouter(
    prefix="/profile", tags=["Profile"]
)


@router.post("",
             response_model=CreateProfileResponse,
             status_code=status.HTTP_201_CREATED
             )
async def create(
        data: CreateProfileRequest,
        use_case: CreateProfile = Depends(CreateProfile),
        current_user: CurrentUser = Depends(get_current_user),
        current_user2: CurrentUser = Depends(get_current_user2),
) -> ProfileSchema:

    try:
        return await use_case.execute(data, current_user2)
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail="Database error occurred"
        )


@router.put("/{profile_id}",
            status_code=status.HTTP_202_ACCEPTED,
            response_model=UpdateProfileResponse,
            )
async def update(
        data: UpdateProfileRequest,
        profile_id: int,
        use_case: UpdateProfile = Depends(UpdateProfile),
        current_user: CurrentUser = Depends(get_current_user)
) -> ProfileSchema:
    return await use_case.execute(profile_id, position=data.position, bio=data.bio)


@router.get("/{id}")
async def read(
        id: int,
        use_case: ReadTeacher = Depends(ReadTeacher),
):
    return await use_case.execute(id)