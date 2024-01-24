import os


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
    0: ('Умеренный', 'green'),
    1: ('Повышенный', 'orange'),
    2: ('Высокий', 'red'),
}
ROUND_DIGITS = 4
REQUEST_DATA_STRUCTURE = {
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
SCORING_CARD_WEIGHTS = {
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
SCORING_CARD_CRITERIA = {
    'current_ratio': [
        (None, 0.80, 10),
        (0.80, 1.20, 50),
        (1.20, None, 100),
    ],
    'equity_ratio': [
        (None, 0.05, 10),
        (0.05, 0.20, 50),
        (0.20, None, 100),
    ],
    'operational_margin': [
        (None, 0.05, 10),
        (0.05, 0.20, 50),
        (0.20, None, 100),
    ],
    'net_margin': [
        (None, 0.0001, 10),
        (0.0001, 0.10, 50),
        (0.10, None, 100),
    ],
    'debt_to_ebitda': [
        (None, 3.00, 10),
        (3.00, 6.00, 50),
        (6.00, None, 100),
    ],
    'fixed_assets_ratio': [
        (None, 0.05, 10),
        (0.05, 0.20, 50),
        (0.20, None, 100),
    ],
    'oper_income_growth': [
        (None, 0.0001, 10),
        (0.0001, 0.10, 50),
        (0.10, None, 100),
    ],
    'contract_weight': [
        (None, 0.10, 10),
        (0.10, 0.33, 50),
        (0.33, None, 100),
    ],
    'net_working_capital_to_contract': [
        (None, 0.10, 10),
        (0.10, 0.50, 50),
        (0.50, None, 100),
    ],
    'experience': [
        (None, 1, 10),
        (1, 3, 50),
        (3, None, 100)
    ],
    'contracts_completed': [
        (None, 2, 10),
        (2, 5, 50),
        (5, None, 100),
    ],
    'license_category': [
        (None, 0, 10),
        (0, 3, 50),
        (3, None, 100)
    ]
}

RISK_LEVEL_MAPPING = [
    (None, 30, 2),
    (30, 80, 1),
    (80, None, 0),
]

# Данные для сохранения скоринга в pdf
DOWN_STEP = 20
X_START_POS = 30
X_END_POS = 570
X_MID_POS = 300
Y_LINE_POS = 790
Y_HEAD_POS = 800
Y_AFTER_LINE_POS = 760
FONT_SIZE_HEADER = 16
FONT_SIZE_NORMAL = 14
REQUEST_ATTRS = ['policyholder', 'contract_number']
REPORT_ATTRS = [
    'current_ratio', 'equity_ratio', 'operational_margin', 'net_margin',
    'debt_to_ebitda', 'fixed_assets_ratio', 'oper_income_growth',
    'contract_weight', 'net_working_capital_to_contract', 'experience',
    'contracts_completed', 'license_category'
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
FILE_READ_ERR_MSG = 'Ошибка при чтении файла'

# Папка со шрифтами
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALIBRI_FONT_PATH = os.path.join(BASE_DIR, 'static', 'fonts', 'calibri.ttf')
CALIBRI_BOLD_FONT_PATH = os.path.join(
    BASE_DIR, 'static', 'fonts', 'calibri_bold.ttf'
)

REQUESTS_PER_PAGE = 20
