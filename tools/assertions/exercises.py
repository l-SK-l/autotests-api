import allure

from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, ExerciseSchema, GetExerciseResponseSchema, GetExercisesResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.errors_schema import InternalErrorResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response

from tools.logger import get_logger

logger = get_logger("EXERCISES_ASSERTIONS")


@allure.step("Verify create exercise response matches request")
def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на создание упражнения соответствует данным из запроса.

    :param request: Исходный запрос на создание упражнения.
    :param response: Ответ API с данными созданного упражнения.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Verify create exercise response matches request")

    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Compare exercise data with expected values")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что модель задания соответствует ожидаемой.

    :param actual: Фактические данные задания.
    :param expected: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Compare exercise data with expected values")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


@allure.step("Verify get exercises response matches created exercises")
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercise_responses: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка упражнений соответствует списку созданных упражнений.

    :param get_exercises_response: Ответ API при запросе списка упражнений.
    :param create_exercise_responses: Список ответов API при создании упражнений.
    :raises AssertionError: Если данные упражнений не совпадают.
    """
    logger.info("Verify get exercises response matches created exercises")

    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)


@allure.step("Verify get exercise response matches created exercise")
def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение задания соответствует ответу на его создание.

    :param get_exercise_response: Ответ API при запросе данных задания.
    :param create_exercise_response: Ответ API при создании задания.
    :raises AssertionError: Если данные задания не совпадают.
    """
    logger.info("Verify get exercise response matches created exercise")

    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


@allure.step("Verify update exercise response matches request")
def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
):
    """
    Проверяет, что ответ на обновление задания соответствует данным из запроса.

    :param request: Исходный запрос на обновление задания.
    :param response: Ответ API с данными обновленного задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Verify update exercise response matches request")

    if request.title is not None:
        assert_equal(response.exercise.title, request.title, "title")
    if request.max_score is not None:
        assert_equal(response.exercise.max_score, request.max_score, "max_score")
    if request.min_score is not None:
        assert_equal(response.exercise.min_score, request.min_score, "min_score")
    if request.order_index is not None:
        assert_equal(response.exercise.order_index, request.order_index, "order_index")
    if request.description is not None:
        assert_equal(response.exercise.description, request.description, "description")
    if request.estimated_time is not None:
        assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Verify exercise not found error response")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Проверяет, что ответ содержит ошибку о ненайденном упражнении.

    :param actual: Фактический ответ API с ошибкой.
    :raises AssertionError: Если сообщение об ошибке не соответствует ожидаемому.
    """
    logger.info("Verify exercise not found error response")

    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)
