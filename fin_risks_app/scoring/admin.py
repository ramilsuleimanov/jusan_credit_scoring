from django.contrib import admin

from fin_scoring.constants import ADMIN_LIST_PER_PAGE
from .models import ScoreReport, ScoreRequest


class ScoreRequestAdmin(admin.ModelAdmin):
    """Настройка вкладки запросов на скоринг в админ панели."""

    list_display = [
        'id', 'policyholder', 'contract_number', 'underwriter', 'created_at'
    ]
    list_display_links = ['policyholder']
    search_fields = ['policyholder']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['-created_at']
    fieldsets = [
        (None, {'fields': [
            'policyholder', 'contract_number', 'contract_date',
            'contract_amount', 'underwriter'
        ]}),
        ('Финансовые показатели', {'fields': [
            'current_assets', 'current_liabilities', 'equity', 'assets',
            'fixed_assets', 'sales', 'oper_income_current',
            'oper_income_previous', 'net_income', 'net_debt',
            'net_interest_expense', 'depreciation', 'income_tax'
        ]}),
        ('Другие показатели', {'fields': [
            'experience', 'contracts_completed', 'license_category',
            'contract_current_outstanding', 'contract_total_outstanding',
        ]}),
    ]


class ScoreReportAdmin(admin.ModelAdmin):
    """Настройка вкладки скоринговых отчетов в админ панели."""

    list_display = [
        'id', 'policyholder', 'contract_number', 'contract_date',
        'contract_amount', 'underwriter', 'created_at'
    ]
    list_display_links = ['id', 'policyholder']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['-created_at']
    fieldsets = [
        (None, {'fields': []}),
        ('Параметры скоринга', {'fields': [
            'current_ratio', 'equity_ratio', 'operational_margin',
            'net_margin', 'debt_to_ebitda', 'experience',
            'contracts_completed', 'fixed_assets_ratio',
            'oper_income_growth', 'license_category', 'contract_weight',
            'net_working_capital_to_contract'
        ]}),
        ('Результат скоринга', {'fields': ['scoring', 'risk_level']}),
    ]

    def policyholder(self, obj):
        """Получает наименование страхователя."""
        return obj.score_request.policyholder

    def contract_number(self, obj):
        """Получает номер контракта."""
        return obj.score_request.contract_number
    
    def contract_date(self, obj):
        """Получает дату контракта."""
        return obj.score_request.contract_date

    def contract_amount(self, obj):
        """Получает сумму контракта."""
        return obj.score_request.contract_amount
    
    def underwriter(self, obj):
        """Получает имя андеррайтера."""
        print(obj.score_request)
        return obj.score_request.underwriter.get_full_name()
    
    policyholder.short_description = 'Страхователь'
    contract_number.short_description = 'Номер контракта'
    contract_date.short_description = 'Дата контракта'
    contract_amount.short_description = 'Сумма контракта'


admin.site.register(ScoreRequest, ScoreRequestAdmin)
admin.site.register(ScoreReport, ScoreReportAdmin)
