import pytest
import string
import random
from faker import Faker
import allure

fake = Faker('ru-RU')

def generate_name():
    generated_name = fake.user_name()
    return generated_name

def generate_password():
    generated_password = fake.password()
    return generated_password

def generate_email():
    generated_email = fake.email()
    return generated_email

@allure.step('Генерируем данные для регистрации пользователя')
def generate_user_body():
    user = {
        'email': generate_email(),
        'name': generate_name(),
        'password': generate_password()
    }
    return user

def generate_random_string(length):
    return ''.join(fake.random_letters(length=length))