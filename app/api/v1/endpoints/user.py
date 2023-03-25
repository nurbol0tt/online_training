from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import DatabaseError
from starlette import status

from app.dto.application import UserSchema
from app.dto.user import (
    ReadUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    ReadAllUserResponse,
    CreateUserResponse,
    CreateUserRequest,
    CurrentUser,
)
from app.service.user import (
    CreateNotebook,
    ReadUser,
    UpdateUser,
    DeleteUser,
    ReadAllUser,
    LoginUser
)

from app.utils.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/user", tags=["User"]
)


@router.post("",
             response_model=CreateUserResponse,
             status_code=status.HTTP_201_CREATED
             )
async def create(
    data: CreateUserRequest,
    use_case: CreateNotebook = Depends(CreateNotebook),
) -> UserSchema:
    try:
        return await use_case.execute(data)
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail="Database error occurred"
        )


@router.get("",
            response_model=ReadAllUserResponse,
            status_code=status.HTTP_200_OK
            )
async def read_all(
        use_case: ReadAllUser = Depends(ReadAllUser),
        current_user: CurrentUser = Depends(get_current_user)
) -> ReadAllUserResponse:
    return ReadAllUserResponse(users=[ue async for ue in use_case.execute()])


@router.get("/{user_id}",
            response_model=ReadUserResponse,
            status_code=status.HTTP_200_OK,
            )
async def read(
        user_id: int,
        use_case: ReadUser = Depends(ReadUser),
        current_user: CurrentUser = Depends(get_current_user)
) -> UserSchema:
    return await use_case.execute(user_id)


@router.put("/{user_id}",
            status_code=status.HTTP_202_ACCEPTED,
            response_model=UpdateUserResponse,
            )
async def update(
        data: UpdateUserRequest,
        user_id: int = Path(..., description=""),
        use_case: UpdateUser = Depends(UpdateUser),
        current_user: CurrentUser = Depends(get_current_user)
) -> UserSchema:
    return await use_case.execute(user_id, name=data.name, email=data.email)


@router.delete("/{user_id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete(
        user_id: int = Path(..., description=""),
        use_case: DeleteUser = Depends(DeleteUser),
        current_user: CurrentUser = Depends(get_current_user)
) -> None:
    await use_case.execute(user_id)


@router.post('/login')
async def auth(request: OAuth2PasswordRequestForm = Depends(),
               use_case: LoginUser = Depends(LoginUser)):
    return await use_case.execute(request)
