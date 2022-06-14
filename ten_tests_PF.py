import pytest
import json
import base64

from api import PetFriends
from setting import valid_email, valid_password, incorrect_email, incorrect_password
import os

pf = PetFriends()


# 1
def test_api_key_with_negativ_email(email=incorrect_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при некорректной почте """

    status, result = pf.get_api_key_with_negativ_email_or_password(email, password)
    assert status == 403
    assert 'key' not in result


# 2
def test_api_key_with_negativ_password(email=incorrect_email, password=incorrect_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при некорректной почте """

    status, result = pf.get_api_key_with_negativ_email_or_password(email, password)
    assert status == 403
    assert 'key' not in result


# 3
def test_add_new_pet_without_photo(name='fuzik', animal_type='parrot', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


# 4
def test_add_pet_photo(pet_photo='images/dog.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet_valid_id(auth_key, pet_id, pet_photo)
    assert status == 200
    assert len(result['pet_photo']) > 0

#5
def test_add_pet_photo_without_photo(pet_photo='no photo here...'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    if type(pet_photo) not in [str]:
        status, _ = pf.add_photo_of_pet_valid_id(auth_key, pet_id, pet_photo)
        assert status == 400

#6
def test_failed_update_self_pet_info(name=765, animal_type='kitty', age= 4):
# тест на проверку ответа ошибки в передачи  данных в name. Должен возвращать код ответа 400, а возвращает код 200, хотя в документации
# в переменной name должени передоваться только str, а в данном случае передан int. Баг в суппорт отправлен.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
        assert result['age'] not in [int]
    else:
        raise Exception("There is no my pets")


#7
def test_add_new_pet_without_photo_incorrect_age(name='fuzik', animal_type='parrot', age='five'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if type(age) in [int]:
        status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
        assert status == 400
        assert result['age'] != [int]


#8
def test_add_new_pet_with_incorrect_name(name=1001, animal_type='dolmatin',
                                     age= 2, pet_photo='images/dog.jpg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if type['name'] in [str]:
        status, result = pf.add_new_pet_valid_data(auth_key, name, animal_type, age, pet_photo)
        assert status == 400
        assert result['name'] != [str]
        print(result)

#9
def test_add_new_pet_with_incorrect_animal_type(name= 'Vladik', animal_type= 5897854558,
                                     age= 2, pet_photo='images/dog.jpg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if type['animal_type'] in [str]:
        status, result = pf.add_new_pet_valid_data(auth_key, name, animal_type, age, pet_photo)
        assert status == 400
        assert result['animal_type'] != [str]
        print(result)

#10
def test_add_new_pet_with_incorrect_age(name= 'Vladik', animal_type= 'dolmatin',
                                     age= 5.5, pet_photo='images/dog.jpg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if type['age'] in [int]:
        status, result = pf.add_new_pet_valid_data(auth_key, name, animal_type, age, pet_photo)

        assert status == 400
        assert result['age'] != [int]
        print(result)