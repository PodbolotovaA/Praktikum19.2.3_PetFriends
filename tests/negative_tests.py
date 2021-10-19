def negative_test_get_all_pets_with_valid_key(filter='ololo'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # ?
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200
    assert "Filter value is incorrect" in result
"""Некорректный фильтр списка"""

def test_delete_nonexistent_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'olololo'
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status != 200, 'Бага'
"""Удаление питомца с несуществущим id"""

def test_get_api_for_user_without_pass(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    assert "This user wasn't found in database" in result
"""Вход с некорректным паролем"""


