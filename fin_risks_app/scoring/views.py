import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .forms import ScoreRequestForm
from .models import ScoreReport, ScoreRequest
from .scoring_calc import get_report_data
from .validators import validate_bin_company, validate_request_data
from companies.models import Company
from fin_scoring.constants import (
    RISK_LEVEL_DICT, CALIBRI_FONT_PATH, CALIBRI_BOLD_FONT_PATH, 
    DOWN_STEP, FONT_SIZE_HEADER,FONT_SIZE_NORMAL,
    X_START_POS, X_END_POS, X_MID_POS, Y_HEAD_POS, Y_LINE_POS,
    Y_AFTER_LINE_POS, REPORT_ATTRS, REQUEST_ATTRS, FILE_READ_ERR_MSG,
    REQUESTS_PER_PAGE
)


CustomUser = get_user_model()


class ScoreRequestListView(LoginRequiredMixin, ListView):
    """Отображает реестр запросов на скоринг."""

    model = ScoreRequest
    template_name = 'scoring/index.html'
    context_object_name = 'requests'
    paginate_by = REQUESTS_PER_PAGE

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
                form.add_error('excel_file', f'{FILE_READ_ERR_MSG}: {e}')
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
        context['risk_level'] = (
            RISK_LEVEL_DICT[int(score_report.risk_level)][0]
        )
        context['risk_level_color'] = (
            RISK_LEVEL_DICT[int(score_report.risk_level)][1]
        )
        return context

@login_required
def download_pdf_report(request, id):
    """Формирует отчет о скоринге в pdf."""
    pdfmetrics.registerFont(TTFont('Calibri', CALIBRI_FONT_PATH))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', CALIBRI_BOLD_FONT_PATH))
    score_request = get_object_or_404(ScoreRequest, id=id)
    if request.user.id != score_request.underwriter.id:
        return render(request, 'errors/403.html', status=403)
    score_report = get_object_or_404(ScoreReport, id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="score_result_{score_report.id}.pdf"'
    )
    pdf = canvas.Canvas(response)
    pdf.setFont('Calibri-Bold', FONT_SIZE_HEADER)
    pdf.drawCentredString(
        X_MID_POS, Y_HEAD_POS, f'Результат скорингового отчета №{score_report.id}'
    )
    pdf.line(X_START_POS, Y_LINE_POS, X_END_POS, Y_LINE_POS)
    pdf.setFont('Calibri', FONT_SIZE_NORMAL)
    y_position = Y_AFTER_LINE_POS
    created_at_local = score_report.created_at.astimezone(
        timezone.get_current_timezone()
    )
    pdf.drawString(
        X_START_POS, Y_AFTER_LINE_POS, (
            f'Дата и время отчета: '
            f'{created_at_local.strftime("%d-%m-%Y %H:%M:%S")}'
        )
    )
    _, y_position = print_attribute(
        ScoreRequest, REQUEST_ATTRS, score_request, y_position, pdf
    )
    y_position -= DOWN_STEP
    pdf.drawString(
        X_START_POS, y_position, 
        f'Дата контракта: {score_request.contract_date.strftime("%d-%m-%Y")}'
    )
    y_position -= DOWN_STEP
    pdf.line(X_START_POS, y_position, X_END_POS, y_position)
    y_position -= DOWN_STEP
    pdf.setFont('Calibri-Bold', FONT_SIZE_NORMAL)
    pdf.drawCentredString(X_MID_POS, y_position, 'Параметры скоринга')
    pdf.setFont('Calibri', FONT_SIZE_NORMAL)
    _, y_position = print_attribute(
        ScoreReport, REPORT_ATTRS, score_report, y_position, pdf
    )
    y_position -= DOWN_STEP
    pdf.line(X_START_POS, y_position, X_END_POS, y_position)
    y_position -= DOWN_STEP
    pdf.setFont('Calibri-Bold', FONT_SIZE_NORMAL)
    pdf.drawCentredString(X_MID_POS, y_position, 'Результаты скоринга')
    y_position -= DOWN_STEP
    pdf.drawString(
        X_START_POS, y_position, f'Скоринговый балл: {score_report.scoring}'
    )
    y_position -= DOWN_STEP
    risk_level = RISK_LEVEL_DICT[int(score_report.risk_level)][0]
    set_risk_level_color(score_report, risk_level, pdf)
    pdf.drawString(
        X_START_POS, y_position, (
            f'Уровень риска: {risk_level}'
        )
    )
    pdf.setFillColor(colors.black)
    y_position -= DOWN_STEP
    pdf.line(X_START_POS, y_position, X_END_POS, y_position)
    y_position -= DOWN_STEP
    pdf.drawString(X_START_POS, y_position, (
        f'Андеррайтер: {score_request.underwriter.first_name} '
        f'{score_request.underwriter.last_name}'
    ))
    pdf.save()
    return response


def print_attribute(score_model, attributes, score_instance, y_position, pdf):
    """Выводит данные аттрибута в pdf отчёт."""
    for attribute in attributes:
        y_position -= DOWN_STEP
        name = score_model._meta.get_field(attribute).verbose_name
        value = getattr(score_instance, attribute)
        pdf.drawString(X_START_POS, y_position, f'{name}: {value}')
    return pdf, y_position


def set_risk_level_color(score_report, risk_level, pdf):
    """Определяет цвет для категории риска."""
    color = RISK_LEVEL_DICT[int(score_report.risk_level)][1]
    return pdf.setFillColor(getattr(colors, color))

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
