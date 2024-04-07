import json
from datetime import datetime

def load_operations():
    """Загрузить операции из файла JSON."""
    with open('../data/operations.json', 'r') as file:
        data = json.load(file)
    return data

def mask_card_number(card_number):
    """Маскировать номер карты."""
    if card_number == None:
        return ""

    parts = card_number.split()
    number = parts[-1]
    masked_number = number[:6] + '*' * 6 + number[-4:]
    number_groups = ' '.join([masked_number[i:i + 4] for i in range(0, len(masked_number), 4)])
    parts[-1] = number_groups
    join_parts = ' '.join(parts)
    return join_parts

def mask_account_number(account_number):
    """Маскировать номер счета."""
    parts = account_number.split()
    number = parts[-1]
    masked_number = '*' * (len(number) - 4) + number[-4:]
    parts[-1] = masked_number
    join_parts = ' '.join(parts)
    return join_parts

def executed_operations():
    """Отфильтровать выполненные операции."""
    executed_operations = []
    for operation in load_operations():
        if operation.get('state') == 'EXECUTED':
            executed_operations.append(operation)
    return executed_operations

def last_5_operations():
    """Получить пять последних выполненных операций."""
    sorted_operations = sorted(executed_operations(), key=lambda x: datetime.fromisoformat(x['date']), reverse=True)
    return sorted_operations[:5]



