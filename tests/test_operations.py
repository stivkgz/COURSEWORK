import pytest
import json
from datetime import datetime
from project.src.operations import load_operations, mask_card_number, mask_account_number,executed_operations, last_5_operations

# Тесты для функции load_operations
# Фикстура для создания временного файла с тестовыми данными
@pytest.fixture
def temp_file(tmp_path):
    test_data = [{'id': 1, 'amount': 100, 'date': '2023-01-01'}, {'id': 2, 'amount': 200, 'date': '2023-01-02'}]
    file_path = tmp_path / "test_operations.json"
    with open(file_path, 'w') as file:
        json.dump(test_data, file)
    return file_path

# Тест на успешную загрузку операций из файла JSON
def test_load_operations_successful(temp_file):
    operations = load_operations(temp_file)
    assert len(operations) == 2
    assert isinstance(operations, list)
    assert all(isinstance(operation, dict) for operation in operations)

# Тест на ошибку при загрузке из несуществующего файла
def test_load_operations_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_operations("non_existing_file.json")

# Тест на ошибку при загрузке из файла с некорректным JSON
def test_load_operations_invalid_json(temp_file):
    with open(temp_file, 'w') as file:
        file.write("invalid json")
    with pytest.raises(json.JSONDecodeError):
        load_operations(temp_file)

# Тесты для функции mask_card_number
def test_mask_card_number_none():
    assert mask_card_number(None) == ""
    assert mask_card_number('Visa Classic 2842878893689012') == 'Visa Classic 2842 87** **** 9012'
    assert mask_card_number('Visa Platinum 1246377376343588') == 'Visa Platinum 1246 37** **** 3588'
    assert mask_card_number('Maestro 3928549031574026') == 'Maestro 3928 54** **** 4026'

# Тесты для функции mask_account_number
def test_mask_account_number():
    assert mask_account_number('Счет 14211924144426031657') == 'Счет ****************1657'
    assert mask_account_number('Счет 84163357546688983493') == 'Счет ****************3493'
    assert mask_account_number('Счет 43597928997568165086') == 'Счет ****************5086'

# Тесты для функции executed_operations
# Фикстура для создания временного файла с тестовыми данными
@pytest.fixture
def temp_file_(tmp_path):
    test_data = [
        {'id': 1, 'amount': 100, 'date': '2023-01-01', 'state': 'EXECUTED'},
        {'id': 2, 'amount': 200, 'date': '2023-01-02', 'state': 'PENDING'},
        {'id': 3, 'amount': 300, 'date': '2023-01-03', 'state': 'EXECUTED'}
    ]
    file_path = tmp_path / "test_operations.json"
    with open(file_path, 'w') as file:
        json.dump(test_data, file)
    return file_path

# Тест на успешное фильтрование выполненных операций
def test_executed_operations_successful(temp_file):
    executed = executed_operations(temp_file)
    assert len(executed) == 0
    assert all(operation['state'] == 'EXECUTED' for operation in executed)

# Тест на ошибку при загрузке из несуществующего файла
def test_executed_operations_file_not_found():
    with pytest.raises(FileNotFoundError):
        executed_operations("non_existing_file.json")

# Тесты для функции last_5_operations
# Фикстура для создания временного файла с тестовыми данными
@pytest.fixture
def temp_file__(tmp_path):
    test_data = [
        {'id': 1, 'amount': 100, 'date': '2023-01-01', 'state': 'EXECUTED'},
        {'id': 2, 'amount': 200, 'date': '2023-01-02', 'state': 'EXECUTED'},
        {'id': 3, 'amount': 300, 'date': '2023-01-03', 'state': 'EXECUTED'},
        {'id': 4, 'amount': 400, 'date': '2023-01-04', 'state': 'EXECUTED'},
        {'id': 5, 'amount': 500, 'date': '2023-01-05', 'state': 'EXECUTED'},
        {'id': 6, 'amount': 600, 'date': '2023-01-06', 'state': 'EXECUTED'},
        {'id': 7, 'amount': 700, 'date': '2023-01-07', 'state': 'EXECUTED'},
        {'id': 8, 'amount': 800, 'date': '2023-01-08', 'state': 'EXECUTED'},
        {'id': 9, 'amount': 900, 'date': '2023-01-09', 'state': 'EXECUTED'},
        {'id': 10, 'amount': 1000, 'date': '2023-01-10', 'state': 'EXECUTED'}
    ]
    file_path = tmp_path / "test_operations.json"
    with open(file_path, 'w') as file:
        json.dump(test_data, file)
    return file_path

# Тест на успешное получение последних 5 выполненных операций
def test_last_5_operations_successful(temp_file__):
    last_5 = last_5_operations(temp_file__)
    assert len(last_5) == 5
    assert last_5[0]['id'] == 10  # Последняя операция в списке
    assert last_5[-1]['id'] == 6   # Первая операция в списке