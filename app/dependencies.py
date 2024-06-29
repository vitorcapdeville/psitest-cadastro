from typing import Annotated

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.settings import Settings, get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def decode_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.PSITEST_AUTH}/users/me", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
