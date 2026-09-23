from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('livros/', views.lista_livros, name='lista'),
    path('livros/novo/', views.novo_livro, name='novo_livro'),
    path('livros/<int:id>/editar/', views.editar_livro, name='editar_livro'),
    path('livros/<int:id>/apagar/', views.apagar_livro, name='apagar_livro'),

    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/novo/', views.novo_autor, name='novo_autor'),
    path('autores/<int:id>/apagar/', views.apagar_autor, name='apagar_autor'),

    path('exemplares/', views.lista_exemplares, name='lista_exemplares'),
    path('exemplares/novo/', views.novo_exemplar, name='novo_exemplar'),
    path('exemplares/<int:id>/apagar/', views.apagar_exemplar, name='apagar_exemplar'),

    path('membros/', views.lista_membros, name='lista_membros'),
    path('membros/novo/', views.novo_membro, name='novo_membro'),
    path('membros/<int:id>/apagar/', views.apagar_membro, name='apagar_membro'),

    path('exemplares/<int:exemplar_id>/emprestar/', views.emprestar_exemplar, name='emprestar_exemplar'),
    path('exemplares/<int:exemplar_id>/devolver/', views.devolver_exemplar, name='devolver_exemplar'),
    path('emprestimos/atrasados/', views.lista_emprestimos_atrasados, name='lista_emprestimos_atrasados'),

    path('exemplares/<int:exemplar_id>/reservar/', views.reservar_exemplar, name='reservar_exemplar'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
]