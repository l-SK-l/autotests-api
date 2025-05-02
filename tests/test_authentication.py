import pytest
from http import HTTPStatus

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema

@pytest.mark.regression
@pytest.mark.authentication
def test_login():
    public_users_client = get_public_users_client()
    authentication_client = get_authentication_client()

    # Создаем пользователя
    create_user_request = CreateUserRequestSchema()
    public_users_client.create_user(create_user_request)

    # Выполняем аутентификацию
    login_request = LoginRequestSchema(
        email=create_user_request.email,
        password=create_user_request.password
    )
    login_response = authentication_client.login_api(login_request)

    # Десериализуем JSON-ответ
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    # Проверяем статус-код
    assert_status_code(login_response.status_code, HTTPStatus.OK)
    # Проверяем, что ответ соответствует ожиданиям
    assert_login_response(login_response_data)
    # Валидируем JSON-схему
    validate_json_schema(login_response.json(), LoginResponseSchema.model_json_schema())

