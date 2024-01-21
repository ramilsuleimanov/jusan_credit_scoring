from datetime import datetime

EMAIL_LENGTH = COMPANY_NAME_LENGTH = 254
(USERNAME_LENGTH, FIRST_NAME_LENGTH, LAST_NAME_LENGTH, PASSWORD_LENGTH,
 CONTRACT_LENGTH) = 150, 150, 150, 150, 150
ADMIN_LIST_PER_PAGE = 20
BIN_LENGTH = RISK_LEVEL_LENGTH = 12
MIN_AMOUNT = 0.0001
LICENSE_CATEGORIES = [
    (0, 'Нет лицензии'),
    (1, 'Лицензия 1 категории'),
    (2, 'Лицензия 2 категории'),
    (3, 'Лицензия 3 категории')
]
LICENSE_CATEGORIES_CHECK = [0, 1, 2, 3]
REQUEST_FILE_UPLOAD_ROOT = 'scoring/requests/'
RISK_LEVEL = [
    (0, 'Умеренный'),
    (1, 'Повышенный'),
    (2, 'Высокий')
]
RISK_LEVEL_DICT = {
    0: 'Умеренный',
    1: 'Повышенный',
    2: 'Высокий',
}
ROUND_DIGITS = 4
request_data_structure = {
    'contract_number': (str, None),
    'contract_date': (None, None),
    'contract_amount': (float, MIN_AMOUNT),
    'current_assets': (float, MIN_AMOUNT),
    'current_liabilities': (float, MIN_AMOUNT),
    'equity': (float, None),
    'assets': (float, MIN_AMOUNT),
    'fixed_assets': (float, MIN_AMOUNT),
    'sales': (float, MIN_AMOUNT),
    'oper_income_current': (float, None),
    'oper_income_previous': (float, None),
    'net_income': (float, None),
    'net_debt': (float, None),
    'net_interest_expense': (float, None),
    'depreciation': (float, None),
    'income_tax': (float, None),
    'experience': (int, MIN_AMOUNT),
    'contracts_completed': (int, MIN_AMOUNT),
    'license_category': (int, None),
    'contract_current_outstanding': (float, MIN_AMOUNT),
    'contract_total_outstanding': (float, MIN_AMOUNT),
}
scoring_card_weights = {
    'current_ratio': 0.10,
    'equity_ratio': 0.10,
    'operational_margin': 0.07,
    'net_margin': 0.08,
    'debt_to_ebitda': 0.10,
    'fixed_assets_ratio': 0.10,
    'oper_income_growth': 0.05,
    'contract_weight': 0.08,
    'net_working_capital_to_contract': 0.07,
    'experience': 0.10,
    'contracts_completed': 0.05,
    'license_category': 0.10
}
scoring_card_criteria = {
    'current_ratio': [
        (None, 0.80, 0),
        (0.80, 1.20, 2),
        (1.20, None, 4),
    ],
    'equity_ratio': [
        (None, 0.05, 0),
        (0.05, 0.20, 2),
        (0.20, None, 4),
    ],
    'operational_margin': [
        (None, 0.05, 0),
        (0.05, 0.20, 2),
        (0.20, None, 4),
    ],
    'net_margin': [
        (None, 0.0001, 0),
        (0.0001, 0.10, 2),
        (0.10, None, 4),
    ],
    'debt_to_ebitda': [
        (None, 3.00, 4),
        (3.00, 6.00, 2),
        (6.00, None, 0),
    ],
    'fixed_assets_ratio': [
        (None, 0.05, 0),
        (0.05, 0.20, 2),
        (0.20, None, 4),
    ],
    'oper_income_growth': [
        (None, 0.0001, 0),
        (0.0001, 0.10, 2),
        (0.10, None, 4),
    ],
    'contract_weight': [
        (None, 0.10, 4),
        (0.10, 0.33, 2),
        (0.33, None, 0),
    ],
    'net_working_capital_to_contract': [
        (None, 0.10, 0),
        (0.10, 0.50, 2),
        (0.50, None, 4),
    ],
    'experience': [
        (None, 1, 0),
        (1, 3, 2),
        (3, None, 4)
    ],
    'contracts_completed': [
        (None, 2, 0),
        (2, 5, 2),
        (5, None, 4),
    ],
    'license_category': [
        (None, 0, 0),
        (0, 3, 4),
        (3, None, 2)
    ]
}

risk_level_mapping = [
    (None, 1.5, 2),
    (1.5, 3.2, 1),
    (3.2, None, 0),
]

# Сообщения об ошибках
BIN_LENGTH_ERR_MSG = 'Введите корректный БИН из 12 цифр.'
BIN_DIGIT_ERR_MSG = 'БИН должен состоять только из цифр'
BIN_UNIQUE_ERR_MSG = 'Компания с таким БИН уже существует.'
BIN_COMPANY_ERR_MSG = 'Не предоставлены БИН или наименование компании.'
BIN_NOT_MATCH_NAME_ERR_MSG = 'БИН в базе данных не совпадает с наименование:'
MIN_AMOUNT_ERR_MSG = 'Значение не может быть меньше 0.'
LICENSE_CATEGORIES_ERR_MSG = (
    'Строительная лицензия может принимать значение только от 0 до 3.'
)
FIELD_MISSING_ERR_MSG = 'В предоставленных данных отсутствует '
FIELD_REDUNDANT_ERR_MSG = 'В предоставленных данных есть лишнее поле '
INCORRECT_TYPE_ERR_MSG = 'Не соответствует тип данных '
