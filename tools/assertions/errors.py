from typing import Any, Sized

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorSchema, ValidationErrorResponseSchema
from tools.assertions.base import assert_equal


def assert_internal_error_response(
        actual: InternalErrorResponseSchema,
        expected: InternalErrorResponseSchema
):
    """
    Функция для проверки внутренней ошибки. Например, ошибки 404 (File not found).

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    assert_equal(actual.details, expected.details, "details")


def assert_length(actual: Sized, expected: Sized, name: str):
    """
    Проверяет, что длины двух объектов совпадают.

    :param name: Название проверяемого объекта.
    :param actual: Фактический объект.
    :param expected: Ожидаемый объект.
    :raises AssertionError: Если длины не совпадают.
    """
    assert len(actual) == len(expected), (
        f'Incorrect object length: "{name}". '
        f'Expected length: {len(expected)}. '
        f'Actual length: {len(actual)}'
    )


def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    """
    Проверяет, что объект ошибки валидации соответствует ожидаемому значению.

    :param actual: Фактическая ошибка.
    :param expected: Ожидаемая ошибка.
    :raises AssertionError: Если значения полей не совпадают.
    """
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")


def assert_validation_error_response(
        actual: ValidationErrorResponseSchema,
        expected: ValidationErrorResponseSchema
):
    """
    Проверяет, что объект ответа API с ошибками валидации (`ValidationErrorResponseSchema`)
    соответствует ожидаемому значению.

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    assert_length(actual.details, expected.details, "details")

    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)

