from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/health", tags=["Health"])


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
            )
async def get():
    return "OK"
