from django.db import models
from django.contrib.auth.models import User  # ou seu próprio model de usuário, se já tiver
from datetime import timedelta


class Autor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    TIPO_CHOICES = [
        ('digital', 'Digital'),
        ('fisico', 'Físico'),
    ]
    CATEGORIA_CHOICES = [
        ('000', '000 – Generalidades e Informação'),
        ('100', '100 – Filosofia e Psicologia'),
        ('200', '200 – Religião e Teologia'),
        ('300', '300 – Ciências Sociais e Direito'),
        ('400', '400 – Linguística e Idiomas'),
        ('500', '500 – Ciências Puras (Exatas e Naturais)'),
        ('600', '600 – Ciências Aplicadas (Tecnologia)'),
        ('700', '700 – Artes e Recreação'),
        ('800', '800 – Literatura'),
        ('900', '900 – História e Geografia'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros')
    ano = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='fisico')
    categoria = models.CharField(max_length=3, choices=CATEGORIA_CHOICES, default='000')

    def __str__(self):
        return self.titulo


class Exemplar(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('emprestado', 'Emprestado'),
        ('reservado', 'Reservado'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='exemplares')
    codigo_patrimonio = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='disponivel')

    def __str__(self):
        return f'{self.livro.titulo} (#{self.codigo_patrimonio})'


class Membro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE, related_name='emprestimos')
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='emprestimos')
    data_emprestimo = models.DateField(auto_now_add=True)
    data_prevista_devolucao = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.exemplar} → {self.membro}'

    @property
    def em_atraso(self):
        from django.utils import timezone
        if self.data_devolucao:
            return self.data_devolucao > self.data_prevista_devolucao
        return timezone.now().date() > self.data_prevista_devolucao

    @property
    def calcular_multa(self):
        from django.utils import timezone
        VALOR_MULTA_POR_DIA = 1.50  

        data_referencia = self.data_devolucao or timezone.now().date()
        dias_atraso = (data_referencia - self.data_prevista_devolucao).days

        if dias_atraso > 0:
            return round(dias_atraso * VALOR_MULTA_POR_DIA, 2)
        return 0.0


class Reserva(models.Model):
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE, related_name='reservas')
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='reservas')
    data_reserva = models.DateTimeField(auto_now_add=True)
    atendida = models.BooleanField(default=False)

    class Meta:
        ordering = ['data_reserva'] 

    def __str__(self):
        return f'{self.membro} aguardando {self.exemplar}'