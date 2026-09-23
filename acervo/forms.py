from django import forms
from datetime import date
from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano', 'tipo', 'categoria']

    def clean_ano(self):
        ano = self.cleaned_data.get('ano')
        ano_atual = date.today().year

        if ano and ano > ano_atual:
            raise forms.ValidationError('Ano Invalido: O ano de publicação não pode ser no futuro.')

        return ano