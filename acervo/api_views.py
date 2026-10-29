from rest_framework import generics
from .models import Livro
from .serializers import LivroSerializer


class LivroListCreate(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    
class LivroDetail(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer