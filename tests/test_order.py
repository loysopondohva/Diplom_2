import allure
import pytest
from methods.order_methods import OrderMethods
import data

class TestOrder:
    @allure.title('Успешное создание заказа с авторизацией')
    def test_create_order_authorized_user_success(self, create_user_and_delete):
        user_data = create_user_and_delete
        token = user_data['access_token']

        order_data = {"ingredients": data.OrderData.INGREDIENTS[:3]}  # Три ингридиента
        response = OrderMethods.order_create(order_data, token)
        expected_data = data.ResponseData.ORDER_CREATION_SUCCESS

        with allure.step('Проверяем ответ'):
            assert response.status_code == expected_data['code'], \
                f"Ожидался код {expected_data['code']}, получен {response.status_code}"

            assert response.json()['success'] == expected_data['success'], \
                f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

            assert response.json()['order']['number'], \
                f"Ожидался Номер заказа но, не получен"


    @allure.title('Успешное создание заказа без авторизации')
    def test_create_order_not_authorized_user_success(self):
        order_data = {"ingredients": data.OrderData.INGREDIENTS[:2]}  # Два ингредиента
        response = OrderMethods.order_create(order_data)
        expected_data = data.ResponseData.ORDER_CREATION_SUCCESS

        with allure.step('Проверяем ответ'):
            assert response.status_code == expected_data['code'], \
                f"Ожидался код {expected_data['code']}, получен {response.status_code}"

            assert response.json()['success'] == expected_data['success'], \
                f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

            assert response.json()['order']['number'], \
                f"Ожидался Номер заказа но, не получен"


    @allure.title('Проверка успешного создания заказа с ингредиентами')
    def test_create_order_with_ingredients_success(self):
        order_data = {"ingredients": data.OrderData.INGREDIENTS[:3]}  # Три ингредиента
        response = OrderMethods.order_create(order_data)
        expected_data = data.ResponseData.ORDER_CREATION_SUCCESS

        with allure.step('Проверяем ответ'):
            assert response.status_code == expected_data['code'], \
                f"Ожидался код {expected_data['code']}, получен {response.status_code}"

            assert response.json()['success'] == expected_data['success'], \
                f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

            assert response.json()['order']['number'], \
                f"Ожидался Номер заказа но, не получен"

    @allure.title('Проверка ошибки при создании заказа с пустым списком ингредиентов')
    @pytest.mark.parametrize('order_data, expected_data, allure_annotation', [
        ({}, data.ResponseData.ORDER_CREATION_FAILED_NO_INGREDIENTS, "без ингредиентов"),                                   # без ингредиентов
        ({"ingredients": []}, data.ResponseData.ORDER_CREATION_FAILED_NO_INGREDIENTS, "с пустым список ингредиентов"),                   # пустой список ингредиентов
     ])
    def test_create_order_wrong_ingredients_failed(self, order_data, expected_data, allure_annotation):
        order_data = order_data
        expected_data = expected_data

        with allure.step(f'Проверяем создание заказа {allure_annotation}'):
            response = OrderMethods.order_create(order_data)

        with allure.step('Проверяем ответ'):
            assert response.status_code == expected_data['code'], \
                f"Ожидался код {expected_data['code']}, получен {response.status_code}"

            assert response.json()['success'] == expected_data['success'], \
                f"Ожидался success-код {expected_data['success']}, получен {response.json()['success']}"

            assert response.json()['message'] == expected_data['message'], \
                f"Ожидалось сообщение {expected_data['message']}, получен {response.json()['message']}"

    @allure.title('Проверка ошибки при создании заказа с неправильным хэшем ингредиента')
    def test_create_order_wrong_ingredient_hash_failed(self):
        order_data = {"ingredients": ["12345678"]}
        expected_data = data.ResponseData.ORDER_CREATION_FAILED_INVALID_INGREDIENT_HASH

        with allure.step(f'Проверяем создание заказа с неверным хешем ингредиентов'):
            response = OrderMethods.order_create(order_data)

        with allure.step('Проверяем ответ'):
            assert response.status_code == expected_data['code'], \
                f"Ожидался код {expected_data['code']}, получен {response.status_code}"
