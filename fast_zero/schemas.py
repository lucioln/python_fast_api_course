from pydantic import BaseModel, EmailStr


class MessageSchema(BaseModel):
    message: str


class UserConstructorSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str


class UserToUpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDBSchema(UserSchema):
    id: int


class UserListSchema(BaseModel):
    users: list[UserPublicSchema]
