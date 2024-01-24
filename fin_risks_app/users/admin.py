from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from fin_scoring.constants import ADMIN_LIST_PER_PAGE


CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Форма для изменения данных пользователя."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False


class CustomUserChangeForm(UserChangeForm):
    """Форма для изменения данных пользователя."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)


class UserAdmin(BaseUserAdmin):
    """Настройка вкладки пользователя в админ панели."""

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['username', 'email', 'first_name', 'last_name']
    list_display_links = ['username']
    search_fields = ['username']
    ordering = ['username']
    list_filter = ['username', 'email']
    list_per_page = ADMIN_LIST_PER_PAGE
    fieldsets = [
        (None, {'fields': [
            'username', 'email', 'password',
        ]}),
        ('Персональное инфо', {'fields': ['first_name', 'last_name']}),
        ('Разрешения', {'fields': ['is_active']}),
    ]
    add_fieldsets = (
        (None, {
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'is_active',
                'password'
            ),
        }),
    )


admin.site.register(CustomUser, UserAdmin)
