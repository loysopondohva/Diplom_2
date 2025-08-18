from os import access
import allure
import requests
import data
import urls

class UserMethods:

    @staticmethod
    @allure.step("Создаём пользователя")
    def user_create(create_body):
        return requests.post(f'{urls.BASE_URL}{urls.USER_CREATE}', json=create_body)

    @staticmethod
    @allure.step("Логинимся пользователем")
    def user_login(login_body):
        return requests.post(f'{urls.BASE_URL}{urls.USER_LOGIN}', json=login_body)

    @staticmethod
    @allure.step("Удаляем пользователя")
    def user_delete(email, password):
        access_token = UserMethods.user_get_token(email, password)
        response = requests.delete(f'{urls.BASE_URL}{urls.USER_DELETE}', headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 202:
            print(f"User {email} deleted successfully.")
        else:
            print(f"Failed to delete user {email}. Response: {response.text}")

    @staticmethod
    @allure.step("Logout пользователя")
    def user_logout(logout_body):
        return requests.post(f'{urls.BASE_URL}{urls.USER_LOGOUT}', json=logout_body)

    @staticmethod
    @allure.step("Получаем токен пользователя")
    def user_get_token(email, password):
        response =  requests.post(f'{urls.BASE_URL}{urls.USER_LOGIN}', json={
            'email': email,
            'password': password
        })
        access_token = response.json()["accessToken"].split(' ')[1]
        return access_token