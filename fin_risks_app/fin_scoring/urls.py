from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path


handler404 = 'scoring.views.page_not_found'
handler400 = 'scoring.views.handler400'
handler500 = 'scoring.views.handler500'

auth_urls = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls)),
    path('', include('scoring.urls')),
]
