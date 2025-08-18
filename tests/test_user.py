import allure
import pytest
from methods.user_methods import UserMethods
import data


class TestUserCreate:
    @allure.title('Тестирование успешного создания уникального пользователя')
    @allure.description('Тут проверяем, что пользователь создается с сгенерированными данными')
    def test_user_create_success(self, create_user_data_and_delete):
        user_data = create_user_data_and_delete
        user_register_body = {"email": user_data["email"],
                              "name": user_data["name"],
                              "password": user_data["password"],
                              }
        with allure.step(f'Создаём пользователя с данными: {user_register_body}'):
            response = UserMethods.user_create(user_register_body)
        expected_data = data.ResponseData.USER_CREATION_SUCCESS

        assert response.status_code == expected_data['code'], \
            f"Ожидался код {expected_data['code']}, получен {response.status_code}"

        assert response.json()['success'] == expected_data['success'], \
            f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

        assert response.json()['accessToken'], \
            f"accessToken не получен"

    @allure.title('Тестирование создания пользователя, который уже зарегистрирован')
    @allure.description('Тут проверяем, что при попытке создать пользователя, который уже существует возникает ошибка')
    def test_user_create_exist_user_failed(self, create_user_and_delete):
        user_data = create_user_and_delete
        user_register_body = {"email": user_data["email"],
                              "name": user_data["name"],
                              "password": user_data["password"],
                              }
        with allure.step(f'Пытаемся повторно создать пользователя с данными: {user_register_body}'):
            response = UserMethods.user_create(user_register_body)
        expected_data = data.ResponseData.USER_CREATION_FAILED_ALREADY_EXIST

        assert response.status_code == expected_data['code'], \
            f"Ожидался код {expected_data['code']}, получен {response.status_code}"

        assert response.json()['success'] == expected_data['success'], \
            f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

        assert response.json()['message'] == expected_data['message'], \
            f"Ожидалось сообщение {expected_data['message']}, получено {response.json()['message']}"

    @allure.title('Тестирование создания пользователя, с недостаточными данными')
    @allure.description('Тут проверяем, что возникает ошибка при попытке создать пользователя с неполными данными')
    @pytest.mark.parametrize('email, password, name', [
             (data.UserData.create_user_email, data.UserData.create_user_password,''),  # пустое поле "name"
            ('', data.UserData.create_user_password, data.UserData.create_user_name),   # пустое поле "email"
            (data.UserData.create_user_email, '', data.UserData.create_user_name),      # пустое поле "password"
        ])
    def test_user_creation_without_login_password_name_failed(self, email, password, name):
        user_register_body = {"email": email,
                            "name": name,
                            "password": password,
                            }

        with allure.step(f'Пытаемся создать пользователя с данными: {user_register_body}'):
            response = UserMethods.user_create(user_register_body)
        expected_data = data.ResponseData.USER_CREATION_FAILED_NO_LOGIN_PASSWORD_NAME

        assert response.status_code == expected_data['code'], \
                f"Ожидался код {expected_data['code']}, получен {response.status_code}"

        assert response.json()['success'] == expected_data['success'], \
            f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

        assert response.json()['message'] == expected_data['message'], \
            f"Ожидалось сообщение {expected_data['message']}, получено {response.json()['message']}"

class TestUserLogin:
    @allure.title('Тестирование авторизации существующего пользователя')
    @allure.description('Тут проверяем, возможен вход в систему существующего пользователя')
    def test_user_login_success(self, create_user_and_delete):
        user_data = create_user_and_delete
        user_login_body = {"email": user_data["email"],
                           "password": user_data["password"],
                          }
        with allure.step(f'Пытаемся авторизоваться пользователем с данными: {user_login_body}'):
            response = UserMethods.user_login(user_login_body)
        expected_data = data.ResponseData.USER_LOGIN_SUCCESS

        assert response.status_code == expected_data['code'], \
            f"Ожидался код {expected_data['code']}, получен {response.status_code}"

        assert response.json()['success'] == expected_data['success'], \
            f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

        assert response.json()['accessToken'], \
            f"accessToken не получен"

    @allure.title('Тестирование выдаваемой ошибки при некорректном логине')
    @allure.description('Тут проверяем, что правильно выдаются ошибки при некорректно указанных логине или пароле в запросе')
    @pytest.mark.parametrize('login_modifier, password_modifier, expected_data', [
             (lambda login: "", lambda pwd: pwd, data.ResponseData.USER_LOGIN_FAILED),        # пустой логин
             (lambda login: login, lambda pwd: "", data.ResponseData.USER_LOGIN_FAILED),      # пустой пароль
             (lambda login: "", lambda pwd: "", data.ResponseData.USER_LOGIN_FAILED),         # пустой логин и пароль
             (lambda login: login + "_wrong", lambda pwd: pwd, data.ResponseData.USER_LOGIN_FAILED),  # неправильный логин
             (lambda login: login, lambda pwd: pwd + "_wrong", data.ResponseData.USER_LOGIN_FAILED)  # неправильный пароль
         ])
    def test_courier_login_invalid_cases_failed(self, login_modifier, password_modifier, expected_data):
        user_data = data.UserData.create_user_body
        email = user_data["email"]
        password = user_data["password"]
        with allure.step(f'Создаём пользователя с данными: {user_data}'):
            UserMethods.user_create(user_data)

        with allure.step('Модифицируем логин и пароль'):
            test_login = login_modifier(email)
            test_password = password_modifier(password)
            login_body = {'email': test_login, 'password': test_password}

        with allure.step(f'Пробуем войти в систему c данными: {login_body}'):
            response = UserMethods.user_login(login_body)

        with allure.step('Проверяем ошибку'):
            assert response.status_code == expected_data['code'], \
                f"Ожидался код {expected_data['code']}, получен {response.status_code}"

            assert response.json()['success'] == expected_data['success'], \
                f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

            assert response.json()['message'] == expected_data['message'], \
                f"Ожидалось сообщение {expected_data['message']}, получено {response.json()['message']}"
