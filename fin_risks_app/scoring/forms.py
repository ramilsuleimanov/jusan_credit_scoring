from django import forms

class ScoreRequestForm(forms.Form):
    """Форма для загрузки запроса на скоринг."""

    excel_file = forms.FileField(
        label='',
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.xls, .xlsx',}),
    )
