from http import HTTPStatus

import pytest

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.fakers import fake
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response as assert_get_user_response
from fixtures.users import UserFixture


@pytest.mark.parametrize("email", ["mail.ru", "gmail.com", "example.com"])
def test_create_user(email: str, public_users_client: PublicUsersClient):
    request = CreateUserRequestSchema(email=fake.email(domain=email))
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_get_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.regression
@pytest.mark.authentication
def test_login(public_users_client: PublicUsersClient, authentication_client: AuthenticationClient):
    create_user_request = CreateUserRequestSchema()
    public_users_client.create_user(create_user_request)

    login_request = LoginRequestSchema(
        email=create_user_request.email,
        password=create_user_request.password
    )
    login_response = authentication_client.login_api(login_request)
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    assert_status_code(login_response.status_code, HTTPStatus.OK)
    assert_login_response(login_response_data)

    validate_json_schema(login_response.json(), login_response_data.model_json_schema())


@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(
    private_users_client: PrivateUsersClient,
    function_user: UserFixture
):
    response = private_users_client.get_user_me_api()
    response_data = GetUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_get_user_response(response_data.user, function_user.response)
