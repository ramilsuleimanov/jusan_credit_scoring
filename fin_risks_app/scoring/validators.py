from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from companies.models import Company
from fin_scoring.constants import (
    BIN_COMPANY_ERR_MSG, BIN_DIGIT_ERR_MSG, BIN_LENGTH,
    BIN_LENGTH_ERR_MSG, LICENSE_CATEGORIES_CHECK, BIN_NOT_MATCH_NAME_ERR_MSG,
    MIN_AMOUNT_ERR_MSG, LICENSE_CATEGORIES_ERR_MSG,
    FIELD_MISSING_ERR_MSG, FIELD_REDUNDANT_ERR_MSG,
    INCORRECT_TYPE_ERR_MSG, request_data_structure
)


def validate_bin_company(bin, name):
    """Проверяет корректность БИН."""
    if not bool(type(bin) == str and type(name) == str):
        return BIN_COMPANY_ERR_MSG
    elif len(bin) != BIN_LENGTH:
        return BIN_LENGTH_ERR_MSG
    for char in bin:
        try:
            int(char)
        except ValueError:
            return BIN_DIGIT_ERR_MSG
    if (
        Company.objects.filter(bin=bin).exists()
        and not Company.objects.filter(bin=bin, name=name)
    ):
        return f'{BIN_NOT_MATCH_NAME_ERR_MSG}: {bin} - {name}'

def validate_request_data(request_data):
    """Проверяет корректность данных в запросе."""
    for item in request_data_structure:
        if item not in request_data:
            return f'{FIELD_MISSING_ERR_MSG} {item}'
    for key, value in request_data.items():
        if key not in request_data_structure:
            return f'{FIELD_REDUNDANT_ERR_MSG} {key}'
        if request_data_structure[key][0]:
            try:
                data_type = request_data_structure[key][0]
                min_value = request_data_structure[key][1]
                request_data[key] = data_type(
                    value
                )
                if data_type == float and min_value and value < min_value:
                    return f'{key} - {MIN_AMOUNT_ERR_MSG}'
            except ValueError:
                return f'{INCORRECT_TYPE_ERR_MSG} {key}'
    if request_data['license_category'] not in LICENSE_CATEGORIES_CHECK:
        return LICENSE_CATEGORIES_ERR_MSG
