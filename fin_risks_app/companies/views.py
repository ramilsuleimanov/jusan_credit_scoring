from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .forms import CompanyBinForm
from .models import Company


class CompanyPostView(LoginRequiredMixin, View):
    """Проверяет наличие компании по БИН."""

    template_name = 'scoring/company.html'

    def get(self, request, *args, **kwargs):
        """Отображает форму для ввода БИН."""
        form = CompanyBinForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Получает наименование компании по БИН."""
        form = CompanyBinForm(request.POST)
        result = None
        if form.is_valid():
            bin = form.cleaned_data['bin']
            try:
                company = Company.objects.get(bin=bin)
                result = company.name
            except Company.DoesNotExist:
                result = f'Компания с {bin} в базе нет'
        return render(request, self.template_name, {
            'form': form,
            'result': result
        })
