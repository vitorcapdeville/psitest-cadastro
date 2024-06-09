from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from fastapi import Body, Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from app.database import criar_db_e_tabelas, engine, get_session
from app.models import User, LoginInfo, UserUpdate

if not database_exists(engine.url):
    criar_db_e_tabelas()


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_user(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).one_or_none()


@app.post("/signup")
async def cadastrar_usuario(
    user: Annotated[LoginInfo, Body(...)],
    name: Annotated[str, Query(...)],
    matricula: Annotated[str, Query(...)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    if get_user(session, user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )
    try:
        emailinfo = validate_email(user.email, check_deliverability=True)
        email = emailinfo.normalized
    except EmailNotValidError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail inválido.",
        )

    db_user = User(
        email=email,
        name=name,
        matricula=matricula,
        verified=False,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Emitir um evento na queue para que a rota de autenticaçao possa pegar
    # A rota de autenticacao vai fazer o hash da senha e vai armazena-la
    # A rota de autenticacao vai enviar um email para o usuario com um link para confirmar o email
    # user.password

    return db_user


@app.get("/users/{email}")
async def get_user_by_email(email: str, session: Session = Depends(get_session)) -> User:
    user = get_user(session, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return user


@app.patch("/heroes/{user_email}")
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
