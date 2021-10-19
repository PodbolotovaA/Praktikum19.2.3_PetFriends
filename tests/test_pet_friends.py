from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

"""Проверка получения ключа"""
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

"""Проверка получения спика всех питомцев"""
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

"""Проверка возможности создания нового питомца с фото"""
def test_add_new_pet_with_valid_data(name='Пёсикус', animal_type='первосозданный',
                                     age='5', pet_photo='images/dog2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

"""Проверка возможности обновления инофрмации о питомце"""
def test_update_self_pet_info(name='Мурзик', animal_type='обновленный', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

"""Проверка возможности удаления питомца"""
def test_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Барбоскин", "двортерьер", "4", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

"""Задание 19.7.2. Часть 1.
Найти методы, которые ещё не реализованы в библиотеке, и написать их реализацию в файле api.py
Напишите ещё 10 различных тестов для данного REST API интерфейса"""

""" №1. Проверка возможности создания нового питомца без фото"""
def test_add_new_pet_without_photo(name='Котик', animal_type='новенький',
                                     age='60'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

""" №2. Проверка возможности добавления фото к созданному питомцу"""
def test_add_pet_photo(pet_photo='images/cat2.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][0]['id']
    # Если запустить предыдущий тест и создать питомца без фото, то из ответа можно скопировать id созданного питомца и
    # добавить фото в его описание. В таком случае строка кода будет выглядеть так:
    # pet_id = '2c5eeac7-eb81-4ece-b091-68f0418f514a'
    status, result = pf.add_photo_for_created_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None
    assert 'jpeg' in result['pet_photo']

""" №3. Проверка получения ключа с некорректным адресом почты"""
def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

""" №4. Проверка получения ключа с некорректным паролем"""
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

""" №5. Проверка возможности создания нового питомца с фото несоответствующего формата"""
def test_add_new_pet_with_invalid_photo_format(name='Догго', animal_type='с плохим фото',
                                     age='5', pet_photo='images/doggo.png'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 500

""" №6. Проверка возможности создания нового питомца с буквами вместо чисел в графе "возраст" (без фото)"""
def test_add_new_pet_with_invalid_age(name='Котик', animal_type='странновозрастной',
                                     age='КОТКОТКОТ'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    """Ожидаемый код ответа - 500, результат - код ответа 200. Негативный тест"""

""" №7. Проверка получения спика питомцев с фильтром my_pets"""
def test_get_my_pets_list(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) == 0 or len(result['pets']) > 0

""" №8. Проверка получения спика питомцев с некорректным фильтром"""
def test_get_invalid_filter_list(filter='invalid_filter'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500

""" №9. Проверка возможности создания нового питомца без заполненных данных"""
def test_add_new_pet_without_data(name='', animal_type='',
                                     age='', pet_photo='images/dog1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    """Ожидаемый код ответа - 500, результат - код ответа 200. Негативный тест"""

""" №10. Проверка возможности создания нового питомца c очень большим количеством символов в имени"""
def test_add_new_pet_without_big_data(name='123456789йцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?*()_+987654321',
                                      animal_type='нечто',
                                     age='1', pet_photo='images/big_cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    """Ожидаемый код ответа - 500, результат - код ответа 200. Негативный тест"""