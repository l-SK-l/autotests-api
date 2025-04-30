from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):  
    """
    Представляет модель данных пользователя.

    Атрибуты:
        id (str): Уникальный идентификатор пользователя.
        email (EmailStr): Адрес электронной почты пользователя.
        last_name (str): Фамилия пользователя.
        first_name (str): Имя пользователя.
        middle_name (str): Отчество пользователя.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserRequestSchema(BaseModel):
    """
    Представляет запрос на создание нового пользователя.

    Атрибуты:
        email (EmailStr): Адрес электронной почты нового пользователя.
        password (str): Пароль нового пользователя.
        last_name (str): Фамилия нового пользователя.
        first_name (str): Имя нового пользователя.
        middle_name (str): Отчество нового пользователя.
    """
    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserResponseSchema(BaseModel):
    """
    Представляет ответ, содержащий данные созданного пользователя.
    """
    user: UserSchema