from project.src.operations import last_5_operations, mask_card_number, mask_account_number
from datetime import datetime

operations = last_5_operations('../data/operations.json')

for operation in operations:
    date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    description = operation['description']
    from_account = operation.get('from')
    if from_account:
        from_account = mask_card_number(from_account)
    elif from_account == None:
        from_account = ''
    to_account = operation.get('to')
    if to_account:
        to_account = mask_account_number(to_account)
    amount = float(operation['operationAmount']['amount'])
    currency = operation['operationAmount']['currency']['name']
    print()
    print(f'{date} {description}\n{from_account} -> {to_account} {amount} {currency}')








