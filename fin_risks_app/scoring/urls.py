from django.urls import include, path

from .views import (
    ScoreRequestDetailView,
    ScoreRequestListView,
    ScoreRequestView
)


app_name = 'scoring'

urlpatterns = [
    path('', ScoreRequestListView.as_view(), name='index'),
    path('make_request/', ScoreRequestView.as_view(), name='make_request'),
    path('requests/<int:pk>', ScoreRequestDetailView.as_view(), name='request_detail'),
]
