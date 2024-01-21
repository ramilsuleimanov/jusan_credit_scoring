from django.core.exceptions import ValidationError

from fin_scoring.constants import (
    BIN_DIGIT_ERR_MSG, BIN_LENGTH, BIN_LENGTH_ERR_MSG
)


def validate_bin(value):
    """Проверяет корректность БИН."""
    if len(value) != BIN_LENGTH:
        raise ValidationError(BIN_LENGTH_ERR_MSG)
    for char in value:
        try:
            int(char)
        except ValueError:
            raise ValidationError(BIN_DIGIT_ERR_MSG)
