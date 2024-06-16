from typing import Annotated

import httpx
from email_validator import EmailNotValidError, validate_email
from fastapi import Query, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from app.database import criar_db_e_tabelas, engine, get_session
from app.models import User, UserUpdate
from app.settings import Settings, get_settings

if not database_exists(engine.url):
    criar_db_e_tabelas()


app = FastAPI()


def get_user(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).one_or_none()


@app.post("/signup")
async def cadastrar_usuario(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    name: Annotated[str, Query(...)],
    matricula: Annotated[str, Query(...)],
    session: Annotated[Session, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> User:
    if get_user(session, form_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )
    try:
        emailinfo = validate_email(form_data.username, check_deliverability=True)
        email = emailinfo.normalized
    except EmailNotValidError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail inválido.",
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.PSITEST_AUTH}/signup", data={"username": form_data.username, "password": form_data.password}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    db_user = User(
        email=email,
        name=name,
        matricula=matricula,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/{email}")
async def get_user_by_email(email: str, session: Session = Depends(get_session)) -> User:
    user = get_user(session, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return user


@app.patch("/users/{user_email}")
def update_hero(user_email: str, user: UserUpdate, session: Session = Depends(get_session)):
    db_user = get_user(session, user_email)
    if not db_user:
        raise HTTPException(status_code=404, detail="E-mail não encontrado.")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
