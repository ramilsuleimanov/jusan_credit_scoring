from django.urls import path

from .views import (
    download_pdf_report,
    ScoreRequestDetailView,
    ScoreRequestListView,
    ScoreRequestView,
)
from companies.views import CompanyPostView


app_name = 'scoring'

urlpatterns = [
    path('', ScoreRequestListView.as_view(), name='index'),
    path('make_request/', ScoreRequestView.as_view(), name='make_request'),
    path(
        'requests/<int:pk>',
        ScoreRequestDetailView.as_view(),
        name='request_detail'
    ),
    path('company/', CompanyPostView.as_view(), name='company'),
    path(
        'requests/<int:id>/download/',
        download_pdf_report,
        name='download_report'
    ),
]
