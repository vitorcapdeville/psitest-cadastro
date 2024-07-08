from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    email: str = Field(primary_key=True, index=True, description="User e-mail")
    name: str = Field(description="User name")
    matricula: str = Field(description="CFP registry number of the user")
    full_name: str | None = Field(default=None, description="User full name")


class UserUpdate(SQLModel):
    name: str | None = Field(default=None, primary_key=True, index=True, description="User e-mail")
    matricula: str | None = Field(default=None, description="CFP registry number of the user")
    full_name: str | None = Field(default=None, description="User full name")
