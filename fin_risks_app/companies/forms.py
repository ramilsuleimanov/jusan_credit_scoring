from django import forms

from .validators import validate_bin

class CompanyBinForm(forms.Form):
    """Форма для получения БИН."""
    bin = forms.CharField(
        label='БИН', 
        max_length=12,
        min_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Введите БИН'}),
        help_text='Введите бизнес идентификационный номер (БИН).',
        validators=[validate_bin]
    )
