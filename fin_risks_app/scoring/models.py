from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from companies.models import Company
from fin_scoring.constants import (
    CONTRACT_LENGTH, LICENSE_CATEGORIES, MIN_AMOUNT, MIN_AMOUNT_ERR_MSG,
    RISK_LEVEL, RISK_LEVEL_LENGTH,
)


CustomUser = get_user_model()


class ScoreRequest(models.Model):
    """Модель для запроса по кредитному скорингу."""

    underwriter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='score_request',
        verbose_name='Андеррайтер',
    )
    policyholder = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='score_request',
        verbose_name='Страхователь',
    )
    contract_number = models.CharField(
        max_length=CONTRACT_LENGTH,
        verbose_name='Номер контракта',
    )
    contract_date = models.DateTimeField(
        verbose_name='Дата контракта',
    )
    contract_amount = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Сумма контракта',
    )
    current_assets = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Краткосрочные активы',
    )
    current_liabilities = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Краткосрочные обязательства',
    )
    equity = models.FloatField(
        default=0,
        verbose_name='Собственный капитал',
    )
    assets = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Активы',
    )
    fixed_assets = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Основные средства',
    )
    sales = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Доход от реализации',
    )
    oper_income_current = models.FloatField(
        default=0,
        verbose_name='Операционная прибыль текущего периода',
    )
    oper_income_previous = models.FloatField(
        default=0,
        verbose_name='Операционная прибыль предыдущего периода',
    )
    net_income = models.FloatField(default=0, verbose_name='Чистая прибыль',)
    net_debt = models.FloatField(default=0, verbose_name='Чистый долг',)
    net_interest_expense = models.FloatField(
        default=0,
        verbose_name='Чистые финансовые расходы',
    )
    depreciation = models.FloatField(
        default=0,
        verbose_name='Амортизация и износ',
    )
    income_tax = models.FloatField(default=0, verbose_name='Расходы по КПН',)
    experience = models.SmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Опыт работы',        
    )
    contracts_completed = models.SmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Количество завершенных контрактов за 2 года',        
    )
    license_category = models.SmallIntegerField(
        choices=LICENSE_CATEGORIES,
        default=0,
    )
    contract_current_outstanding = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Остаток денег по контракту',        
    )
    contract_total_outstanding = models.FloatField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Остаток денег по реестру контрактов',        
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Создано/обновлено',
    )

    class Meta:
        verbose_name = 'Заявка на скоринг'
        verbose_name_plural = 'Заявки на скоринг'
        ordering = ['-created_at']


class ScoreReport(models.Model):
    """Модель для отчета по кредитному скорингу."""

    score_request = models.ForeignKey(
        ScoreRequest,
        on_delete=models.CASCADE,
        related_name='score_report',
        verbose_name='Запрос на скоринг',
    )
    current_ratio = models.FloatField(
        verbose_name='Коэффициент текущей ликвидности',
    )
    equity_ratio = models.FloatField(
        verbose_name='Коэффициент автономии',
    )
    operational_margin = models.FloatField(
        verbose_name='Маржа операционной прибыли',
    )
    net_margin = models.FloatField(
        verbose_name='Маржа чистой прибыли',
    )
    debt_to_ebitda = models.FloatField(
        verbose_name='Коэффициент Долг/EBITDA',
    )
    experience = models.SmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Опыт работы',        
    )
    contracts_completed = models.SmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERR_MSG,
            )
        ],
        default=0,
        verbose_name='Количество завершенных контрактов за 2 года',        
    )
    fixed_assets_ratio = models.FloatField(
        verbose_name='Доля основных средств в активах',
    )
    oper_income_growth = models.FloatField(
        verbose_name='Прирост операционной прибыли',
    )
    license_category = models.SmallIntegerField(
        verbose_name='Категория лицензии',
        choices=LICENSE_CATEGORIES,
        default=0,
    )
    contract_weight = models.FloatField(
        verbose_name='Доля страхуемого контракта',
    )
    net_working_capital_to_contract = models.FloatField(
        verbose_name='СОК к сумме страхуемого контракта',
    )
    scoring = models.FloatField(
        verbose_name='Скоринг',
    )
    risk_level = models.CharField(
        max_length=RISK_LEVEL_LENGTH,
        choices=RISK_LEVEL,
        verbose_name='Уровень риска',
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Создано/обновлено',
    )

    class Meta:
        verbose_name = 'Скоринговый отчет'
        verbose_name_plural = 'Скоринговые отчеты'
        ordering = ['-created_at']
