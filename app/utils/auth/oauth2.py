from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.utils.auth.my_token import verify_token, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)


def get_current_user2(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        if username is None:
            raise HTTPException(status_code=404, detail="User not found")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

