from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_get_db
from app.dto.user import UserCreate

router = APIRouter(
    prefix="/v1",
    tags=["health"]
)


@router.get("",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "model": str,
                    "content": {
                        "text/plain": {
                            "example": "OK"
                        }
                    }
                }
            },
            response_class=PlainTextResponse)
async def get():
    return "OK"

