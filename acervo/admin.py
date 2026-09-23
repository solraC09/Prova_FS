from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'ano', 'tipo', 'categoria', 'disponivel')
    list_filter = ('tipo', 'categoria', 'disponivel')