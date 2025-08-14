# Основной URL сервера
BASE_URL = 'https://stellarburgers.nomoreparties.site'

# Создание пользователя
USER_CREATE = '/api/auth/register'
# Логин пользователя в систему
USER_LOGIN = '/api/auth/login'
# Логаут пользователя из системы
USER_LOGOUT = 'api/auth/logout'
# Обновление токена пользователя
USER_TOKEN_REFRESH = '/api/auth/token'
# Удаление пользователя
USER_DELETE = '/api/auth/user'


# Создание заказа
CREATE_ORDER = '/api/orders'
# Получение списка заказов
GET_ORDERS = '/api/orders/all'
# Отмена заказа
CANCEL_ORDER = '/api/v1/orders/cancel'

# Получение списка ингредиентов
GET_INGREDIENTS = '/api/ingredients'
