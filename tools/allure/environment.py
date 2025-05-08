import platform
import sys
from config import settings


def create_allure_environment_file():
    # Получаем информацию об операционной системе и версии Python
    os_info = f'{platform.system()}, {platform.release()}'
    python_version = sys.version

    # Создаем словарь с базовыми настройками из settings
    env_data = settings.model_dump()

    # Добавляем информацию об ОС и версии Python
    env_data['os_info'] = os_info
    env_data['python_version'] = python_version

    # Создаем список из элементов в формате {key}={value}
    items = [f'{key}={value}' for key, value in env_data.items()]
    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # Открываем файл ./allure-results/environment.properties на чтение
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)  # Записываем переменные в файл