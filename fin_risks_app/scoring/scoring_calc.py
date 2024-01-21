from fin_scoring.constants import (
    ROUND_DIGITS, scoring_card_criteria, scoring_card_weights,
    risk_level_mapping
)


def get_report_data(request_data):
    """Расчитывает параметры для скоринга."""
    report_data = {}
    report_data['current_ratio'] = round(
        request_data['current_assets']
        / request_data['current_liabilities'], ROUND_DIGITS
    )
    report_data['equity_ratio'] = round(
        request_data['equity'] / request_data['assets'], ROUND_DIGITS
    )
    report_data['operational_margin'] = round(
        request_data['oper_income_current']
        / request_data['sales'], ROUND_DIGITS
    )
    report_data['net_margin'] = round(
        request_data['net_income'] / request_data['sales'], ROUND_DIGITS
    )
    report_data['debt_to_ebitda'] = round(
        request_data['net_debt'] / (
            request_data['net_income']
            + (-request_data['income_tax'])
            + (-request_data['net_interest_expense'])
            + (-request_data['depreciation'])
        ), ROUND_DIGITS
    )
    report_data['experience'] = request_data['experience']
    report_data['contracts_completed'] = request_data['contracts_completed']
    report_data['fixed_assets_ratio'] = round(
        request_data['fixed_assets'] / request_data['assets'], ROUND_DIGITS
    )
    report_data['oper_income_growth'] = round(
        request_data['oper_income_current']
        / request_data['oper_income_previous'], ROUND_DIGITS
    )
    report_data['license_category'] = request_data['license_category']
    report_data['contract_weight'] = round(
        request_data['contract_current_outstanding']
        / request_data['contract_total_outstanding'], ROUND_DIGITS
    )
    report_data['net_working_capital_to_contract'] = round(
        (request_data['current_assets'] - request_data['current_liabilities'])
        / request_data['contract_current_outstanding'], ROUND_DIGITS
    )
    report_data = calculate_scoring(report_data)
    return report_data


def calculate_scoring(report_data):
    """Расчитывает скоринговый балл и уровень риска."""
    scoring = 0
    for parameter in report_data:
        parameter_value = report_data[parameter]
        weight = scoring_card_weights[parameter]
        criteria = scoring_card_criteria[parameter]
        if not criteria[0][0] and parameter_value <= criteria[0][1]:
            parameter_score = criteria[0][2]
        elif not criteria[2][1] and parameter_value > criteria[2][0]:
            parameter_score = criteria[2][2]
        else:
            parameter_score = criteria[1][2]
        scoring += parameter_score * weight
    report_data['scoring'] = round(scoring, 4)
    report_data['risk_level'] = get_risk_level(scoring)
    return report_data


def get_risk_level(scoring):
    """Определяет уровень риска страхователя."""
    if not risk_level_mapping[0][0] and scoring <= risk_level_mapping[0][1]:
        risk_level = risk_level_mapping[0][2]
    elif not risk_level_mapping[2][1] and scoring > risk_level_mapping[2][0]:
        risk_level = risk_level_mapping[2][2]
    else:
        risk_level = risk_level_mapping[1][2]
    return risk_level


