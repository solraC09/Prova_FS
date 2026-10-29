from django.urls import path
from .api_views import LivroListCreate, LivroDetail


urlpatterns = [
    path('livros/', LivroListCreate.as_view()),
    path('livros/<int:pk>/', LivroDetail.as_view()),
]
