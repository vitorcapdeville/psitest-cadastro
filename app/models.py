from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    email: str = Field(primary_key=True, index=True)
    name: str
    matricula: str
    full_name: str | None = None


class UserUpdate(SQLModel):
    name: str | None = None
    matricula: str | None = None
    full_name: str | None = None
