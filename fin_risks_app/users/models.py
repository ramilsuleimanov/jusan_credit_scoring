from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from fin_scoring.constants import (
    FIRST_NAME_LENGTH, LAST_NAME_LENGTH, USERNAME_LENGTH
)


class CustomUserManager(UserManager):
    """Менеджер по созданию кастомного пользотваля."""

    pass


class CustomUser(AbstractUser):
    """Кастомизированная модель пользователя."""

    REQUIRED_FIELDS = ['first_name', 'last_name']

    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с таким никнеймом уже зарегистрирован.',
        },
        verbose_name='Никнейм',
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже зарегистрирован',
        },
        verbose_name='email',
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_LENGTH,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=LAST_NAME_LENGTH,
        verbose_name='Фамилия',
    )
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['username']

    def __str__(self):
        """Выводит имя пользователя."""
        return self.username

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь админом."""
        return self.is_superuser
