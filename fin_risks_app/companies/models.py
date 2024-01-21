from django.db import models

from fin_scoring.constants import (
    BIN_LENGTH, BIN_UNIQUE_ERR_MSG, COMPANY_NAME_LENGTH
)
from .validators import validate_bin

class Company(models.Model):
    """Модель для компаний."""

    name = models.CharField(
        max_length=COMPANY_NAME_LENGTH,
        verbose_name='Наименование компании',
    )
    bin = models.CharField(
        max_length=BIN_LENGTH,
        unique=True,
        error_messages={
            'unique': BIN_UNIQUE_ERR_MSG,
        },
        validators=[validate_bin],
        verbose_name='БИН',
    )

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'
        ordering = ['name']
    
    def __str__(self):
        return self.name
