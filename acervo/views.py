from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import Livro, Autor, Exemplar, Membro, Emprestimo, Reserva
from .forms import LivroForm


def inicio(request):
    return render(request, 'acervo/inicio.html')


def lista_livros(request):
    livros = Livro.objects.all()

    nome = request.GET.get('nome', '')
    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')

    if nome:
        livros = livros.filter(titulo__icontains=nome)
    if tipo:
        livros = livros.filter(tipo=tipo)
    if categoria:
        livros = livros.filter(categoria=categoria)

    return render(request, 'acervo/lista.html', {
        'livros': livros,
        'tipos': Livro.TIPO_CHOICES,
        'categorias': Livro.CATEGORIA_CHOICES,
        'filtro_nome': nome,
        'filtro_tipo': tipo,
        'filtro_categoria': categoria,
    })


def novo_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = LivroForm()

    return render(request, 'acervo/form.html', {'form': form})


def editar_livro(request, id):
    livro = get_object_or_404(Livro, id=id)

    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = LivroForm(instance=livro)

    return render(request, 'acervo/form.html', {'form': form})


def apagar_livro(request, id):
    livro = get_object_or_404(Livro, id=id)

    if request.method == 'POST':
        livro.delete()
        return redirect('lista')

    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': livro})


def lista_exemplares(request):
    exemplares = Exemplar.objects.select_related('livro').all()
    return render(request, 'acervo/exemplares/lista.html', {'exemplares': exemplares})


def novo_exemplar(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro')
        codigo = request.POST.get('codigo_patrimonio')
        livro = get_object_or_404(Livro, id=livro_id)
        Exemplar.objects.create(livro=livro, codigo_patrimonio=codigo)
        return redirect('lista_exemplares')

    livros = Livro.objects.all()
    return render(request, 'acervo/exemplares/form.html', {'livros': livros})


def apagar_exemplar(request, id):
    exemplar = get_object_or_404(Exemplar, id=id)

    if request.method == 'POST':
        exemplar.delete()
        return redirect('lista_exemplares')

    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': exemplar})


def lista_membros(request):
    membros = Membro.objects.all()
    return render(request, 'acervo/membros/lista.html', {'membros': membros})


def novo_membro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        Membro.objects.create(nome=nome, email=email)
        return redirect('lista_membros')

    return render(request, 'acervo/membros/form.html')


def apagar_membro(request, id):
    membro = get_object_or_404(Membro, id=id)

    if request.method == 'POST':
        membro.delete()
        return redirect('lista_membros')

    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': membro})


def emprestar_exemplar(request, exemplar_id):
    exemplar = get_object_or_404(Exemplar, id=exemplar_id)

    if request.method == 'POST':
        membro_id = request.POST.get('membro')
        membro = get_object_or_404(Membro, id=membro_id)

        if exemplar.status != 'disponivel':
            # já está emprestado ou reservado para outra pessoa
            return redirect('lista_exemplares')

        Emprestimo.objects.create(
            exemplar=exemplar,
            membro=membro,
            data_prevista_devolucao=timezone.now().date() + timedelta(days=14),
        )
        exemplar.status = 'emprestado'
        exemplar.save()
        return redirect('lista_exemplares')

    membros = Membro.objects.all()
    return render(request, 'acervo/emprestimos/form.html', {
        'exemplar': exemplar,
        'membros': membros,
    })


def devolver_exemplar(request, exemplar_id):
    exemplar = get_object_or_404(Exemplar, id=exemplar_id)

    if request.method == 'POST':
        emprestimo = exemplar.emprestimos.filter(data_devolucao__isnull=True).first()
        if emprestimo:
            emprestimo.data_devolucao = timezone.now().date()
            emprestimo.save()

        proxima_reserva = exemplar.reservas.filter(atendida=False).first()

        if proxima_reserva:
            exemplar.status = 'reservado'
        else:
            exemplar.status = 'disponivel'
        exemplar.save()

        return redirect('lista_exemplares')

    return render(request, 'acervo/emprestimos/confirmar_devolucao.html', {'exemplar': exemplar})


def lista_emprestimos_atrasados(request):
    atrasados = Emprestimo.objects.filter(
        data_devolucao__isnull=True,
        data_prevista_devolucao__lt=timezone.now().date(),
    ).select_related('exemplar', 'exemplar__livro', 'membro')

    return render(request, 'acervo/emprestimos/atrasados.html', {'emprestimos': atrasados})


def reservar_exemplar(request, exemplar_id):
    exemplar = get_object_or_404(Exemplar, id=exemplar_id)

    if request.method == 'POST':
        membro_id = request.POST.get('membro')
        membro = get_object_or_404(Membro, id=membro_id)

        Reserva.objects.create(exemplar=exemplar, membro=membro)
        return redirect('lista_exemplares')

    membros = Membro.objects.all()
    return render(request, 'acervo/reservas/form.html', {
        'exemplar': exemplar,
        'membros': membros,
    })


def lista_reservas(request):
    reservas = Reserva.objects.filter(atendida=False).select_related('exemplar', 'membro')
    return render(request, 'acervo/reservas/lista.html', {'reservas': reservas})

def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'acervo/autores/lista.html', {'autores': autores})


def novo_autor(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        Autor.objects.create(nome=nome)
        return redirect('lista_autores')

    return render(request, 'acervo/autores/form.html')


def apagar_autor(request, id):
    autor = get_object_or_404(Autor, id=id)

    if request.method == 'POST':
        autor.delete()
        return redirect('lista_autores')

    return render(request, 'acervo/confirmar_exclusao.html', {'objeto': autor})