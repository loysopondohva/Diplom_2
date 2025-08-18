import allure
import requests
import data
import urls


class OrderMethods:
    @staticmethod
    @allure.step("Создаём заказ")
    def order_create(order_body, token = None):
        headers = {}
        if token:
            headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(f'{urls.BASE_URL}{urls.CREATE_ORDER}', json=order_body, headers=headers)
        return response

    @staticmethod
    @allure.step("Получаем список заказов")
    def get_orders_list():
        return requests.get(f'{urls.BASE_URL}{urls.GET_ORDERS}')