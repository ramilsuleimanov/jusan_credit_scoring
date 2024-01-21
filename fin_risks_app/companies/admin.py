from django.contrib import admin

from fin_scoring.constants import ADMIN_LIST_PER_PAGE
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    """Настройка вкладки ингридиентов в админ панели."""

    list_display = ['id', 'name', 'bin']
    list_display_links = ['name']
    search_fields = ['name', 'bin']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['name']


admin.site.register(Company, CompanyAdmin)
