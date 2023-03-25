from fastapi import APIRouter, File, UploadFile, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.dto.user import CurrentUser
from app.utils.auth.oauth2 import get_current_user, get_current_user2

from app.service.profile_photo import (
    CreateProfilePhoto,
    ReadProfilePhoto, UpdateProfilePhotoUser, DeleteProfilePhoto
)

router = APIRouter(
    prefix="/profile/photo", tags=["Profile Photo"]
)


@router.post("",
             status_code=status.HTTP_201_CREATED
             )
async def create(
        file: UploadFile = File(...),
        use_case: CreateProfilePhoto = Depends(CreateProfilePhoto),
        current_user: CurrentUser = Depends(get_current_user),
        current_user2: CurrentUser = Depends(get_current_user2),
) -> JSONResponse:

    photo = await file.read()
    await use_case.execute(photo, current_user2)

    message = {"success": True, "message": f"Photo successfully created. URL"}
    return JSONResponse(content=message, status_code=status.HTTP_201_CREATED)


@router.get("/{photo_id}",
            status_code=status.HTTP_200_OK,
            )
async def read_photo(
        photo_id: int,
        use_case: ReadProfilePhoto = Depends(ReadProfilePhoto),
):
    return await use_case.execute(photo_id)


@router.put("/{photo_id}",
            status_code=status.HTTP_202_ACCEPTED,
            )
async def update(
        file: UploadFile = File(...),
        use_case: UpdateProfilePhotoUser = Depends(UpdateProfilePhotoUser),
        current_user: CurrentUser = Depends(get_current_user),
        current_user2: CurrentUser = Depends(get_current_user2),
):
    photo = await file.read()

    return await use_case.execute(photo, current_user2)


@router.delete("",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        use_case: DeleteProfilePhoto = Depends(DeleteProfilePhoto),
        current_user: CurrentUser = Depends(get_current_user),
        current_user2: CurrentUser = Depends(get_current_user2),
) -> None:
    await use_case.execute(current_user2)