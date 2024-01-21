import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse
from django.views import View
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, TemplateView,
)

from .forms import ScoreRequestForm
from .models import ScoreReport, ScoreRequest
from .scoring_calc import get_report_data
from .validators import validate_bin_company, validate_request_data
from companies.models import Company
from fin_scoring.constants import RISK_LEVEL_DICT


CustomUser = get_user_model()


class ScoreRequestListView(LoginRequiredMixin, ListView):
    """Отображает реестр запросов на скоринг."""

    model = ScoreRequest
    template_name = 'scoring/index.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return ScoreRequest.objects.filter(
            underwriter=self.request.user,
        )


class ScoreRequestView(LoginRequiredMixin, View):
    """Загружает excel файл с запросом на скоринг и сохраняет данные."""

    template_name = 'scoring/make_request.html'

    def get(self, request, *args, **kwargs):
        """Получает форму для запроса."""
        form = ScoreRequestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Обрабатывает форму с запросом и сохраняет данные в базу."""
        form = ScoreRequestForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file, sheet_name='scoring_data')
            except pd.errors.ParserError as e:
                form.add_error('excel_file', f'Ошибка при чтении файла: {e}')
                return render(request, self.template_name, {'form': form})
            request_data = dict(zip(df['field'], df['amount']))
            bin = request_data.pop('bin')
            name = request_data.pop('policyholder')
            bin_company_error = validate_bin_company(bin, name)
            if bin_company_error:
                form.add_error(None, bin_company_error)
                return render(request, self.template_name, {'form': form})
            request_data_error = validate_request_data(request_data)
            if request_data_error:
                form.add_error(None, request_data_error)
                return render(request, self.template_name, {'form': form})
            policyholder, created = Company.objects.get_or_create(
                name=name, bin=bin
            )
            request_data['contract_date'] = timezone.make_aware(
                request_data['contract_date']
            )
            score_request = ScoreRequest.objects.create(
                underwriter=request.user,
                policyholder=policyholder,
                **request_data,
            )
            report_data = get_report_data(request_data)
            ScoreReport.objects.create(
                score_request=score_request,
                **report_data,
            )
            return redirect(reverse('scoring:index'))
        else:
            return render(request, self.template_name, {'form': form})


class ScoreRequestDetailView(LoginRequiredMixin, DetailView):
    """Выводит детали запроса на скоринг."""

    model = ScoreRequest
    template_name = 'scoring/request_detail.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        score_request_id = kwargs.get('object').id
        score_report = get_object_or_404(
            ScoreReport, score_request_id=score_request_id
        )
        context['scoring'] = score_report.scoring
        context['risk_level'] = RISK_LEVEL_DICT[int(score_report.risk_level)]
        return context


def page_not_found(request, exception):
    """Renders 404 Not Found Page."""
    return render(request, 'errors/404.html', status=404)


def csrf_failure(request, reason=''):
    """Renders 403 Error Page."""
    return render(request, 'errors/403csrf.html', status=403)


def handler500(request):
    """Renders 500 Internal Server Error Page."""
    return render(request, 'errors/500.html', status=500)


def handler400(request, exception):
    """Renders 400 Bad Request Page."""
    return render(request, 'errors/400.html', status=400)
