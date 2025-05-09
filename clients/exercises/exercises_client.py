import allure
from httpx import Response

from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseResponseSchema, GetExercisesQuerySchema, GetExercisesResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from tools.routes import APIRoutes


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    @allure.step("Get exercises list with query parameters")
    @tracker.track_endpoint(f"{APIRoutes.EXERCISES}")
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Метод получения списка упражнений.

        :param query: Словарь с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.EXERCISES}", params=query.model_dump(by_alias=True))

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    @allure.step("Get exercise by ID {exercise_id}")
    @tracker.track_endpoint(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения упражнения.

        :param exercise_id: Идентификатор упражнения.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Create new exercise")
    @tracker.track_endpoint(f"{APIRoutes.EXERCISES}")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Метод создания упражнения.

        :param request: Словарь с title, courseId, maxScore, minScore, orderIndex,
        description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(f"{APIRoutes.EXERCISES}", json=request.model_dump(by_alias=True))

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Update exercise with ID {exercise_id}")
    @tracker.track_endpoint(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def update_exercise_api(self, exercise_id: str,
                             request: UpdateExerciseRequestSchema) -> Response:
        """
        Метод обновления упражнения.

        :param exercise_id : Идентификатор упражнения.
        :param request: Словарь с title, maxScore, minScore, orderIndex,
        description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"{APIRoutes.EXERCISES}/{exercise_id}", json=request.model_dump(by_alias=True))

    def update_exercise(self, exercise_id: str,
                         request: UpdateExerciseRequestSchema) -> UpdateExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Delete exercise with ID {exercise_id}")
    @tracker.track_endpoint(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления упражнения.

        :param exercise_id: Идентификатор упражнения.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.EXERCISES}/{exercise_id}")

    def delete_exercise(self, exercise_id: str) -> None:
        self.delete_exercise_api(exercise_id)


def create_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))
