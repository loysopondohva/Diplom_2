import generators


class UserData:
    create_user_body = generators.generate_user_body()
    create_user_name = generators.generate_name()
    create_user_email = generators.generate_email()
    create_user_password = generators.generate_password()

    random_user_login_data = {'email': generators.generate_email(), 'password': generators.generate_password()}

class OrderData:
    INGREDIENTS = [
        "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка R2-D3
        "61c0c5a71d1f82001bdaaa6f",  # Мясо бессмертных моллюсков Protostomia
        "61c0c5a71d1f82001bdaaa70",  # Говяжий метеорит (отбивная)
        "61c0c5a71d1f82001bdaaa71",  # Биокотлета из марсианской Магнолии
        "61c0c5a71d1f82001bdaaa72",  # Соус Spicy-X
        "61c0c5a71d1f82001bdaaa6e",  # Филе Люминесцентного тетраодонтимформа
        "61c0c5a71d1f82001bdaaa73",  # Соус фирменный Space Sauce
    ]


class ResponseData:
    USER_CREATION_SUCCESS = {
        "code": 200,
        "success": True,
    }

    USER_CREATION_FAILED_NO_LOGIN_PASSWORD_NAME = {
        "code": 403,
        "success": False,
        "message": "Email, password and name are required fields"
    }
    USER_CREATION_FAILED_ALREADY_EXIST = {
        "code": 403,
        "success": False,
        "message": "User already exists"
    }

    USER_LOGIN_SUCCESS = {
        "code": 200,
        "success": True
    }
    USER_LOGIN_FAILED = {
        "code": 401,
        "success": False,
        "message": "email or password are incorrect"
    }

    USER_LOGOUT_SUCCESS = {
        "success": True,
        "message": "Successful logout"
    }

    ORDER_CREATION_SUCCESS = {
        "code": 200,
        "success": True,
    }

    ORDER_CREATION_FAILED_NO_INGREDIENTS = {
        "code": 400,
        "success": False,
        "message": "Ingredient ids must be provided"
    }


    ORDER_CREATION_FAILED_INVALID_INGREDIENT_HASH = {
        "code": 500
    }