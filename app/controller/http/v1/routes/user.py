from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.user import Login, UserBase
from app.utils.auth import my_token
from app.utils.auth.hashing import Hasher
from app.db.database import async_get_db
from app.dto import user
from app.entity.user import User
from app.utils.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: user.UserCreate,
                      db: AsyncSession = Depends(async_get_db),
                      current_user: UserBase = Depends(get_current_user)
                      ):

    queryset = User(name=request.name, email=request.email, password=Hasher.bcrypt(request.password))
    db.add(queryset)
    db.commit()
    db.refresh(queryset)
    return queryset


@router.get('/{id}', response_model=user.ShowUser)
async def get_user(id: int, db: AsyncSession = Depends(async_get_db),
                   current_user: UserBase = Depends(get_current_user)
                   ):
    statement = select(User).filter(User.id == id)
    result = await db.execute(statement)
    queryset = result.scalar_one_or_none()

    if not queryset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} not found"
        )

    return queryset


@router.post('/login')
async def auth(request: OAuth2PasswordRequestForm = Depends(),
               db: AsyncSession = Depends(async_get_db)):
    statement = select(User).filter(User.email == request.username)
    result = await db.execute(statement)
    queryset = result.scalar_one_or_none()

    if not queryset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hasher.verify_password(queryset.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = await my_token.create_access_token(data={"sub": queryset.name})
    return {"access_token": access_token, "token_type": "bearer"}

