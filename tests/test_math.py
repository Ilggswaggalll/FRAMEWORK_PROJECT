import pytest


# test_math.py
def add_sum(a, b):
    return a + b

# маркируем как смоук-тест
@pytest.mark.smoke
def test_add():
    assert add_sum(2, 3) == 5, 'сумма не равна ожидаемой'

# маркируем как регрессионный тест
def test_type_result():
    assert isinstance(add_sum(2, 3), int), \
        'не соответствует ожидаемому типу данных'