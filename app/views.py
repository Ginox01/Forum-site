from django.shortcuts import render ,HttpResponseRedirect , get_object_or_404 ,HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import DeleteView

from .models import Sezione , Discussione , Post
from .forms import RegistrazioneUserForm , CreaSezioneForm , CreaDiscussioneForm , CreaPostForm

# Create your views here.


def homepage(request):
    sezioni = Sezione.objects.all()
    context = {'sezioni':sezioni}
    return render(request,'index.html',context)

def registrazione_user(request):
    if request.method == 'POST':
        form = RegistrazioneUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user = authenticate(username=username,password=password)
            login(request,user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrazioneUserForm()
    context = {'form':form}
    return render(request,'registrazione_utente.html',context)

def user_profile(request,username):
    user = get_object_or_404(User,username=username)
    context = {'user':user}
    return render(request,'user_profile.html',context)

def users(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request,'users.html',context)



def create_section(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CreaSezioneForm(request.POST , request.FILES)
            if form.is_valid():
                nome = form.cleaned_data['nome']
                descrizione = form.cleaned_data['descrizione']
                immagine = form.cleaned_data['immagine']
                sezione = Sezione.objects.create(
                    nome=nome,
                    descrizione=descrizione,
                    immagine=immagine
                )
                sezione.save()
                return HttpResponseRedirect('/')
        else:
            form = CreaSezioneForm()
        context = {'form':form}
        return render(request,'create_section.html',context)
    else:
        return HttpResponse('<h1><br>Spiacente , pagina riservata allo staff</h1>')


def section(request,pk):
    sezione = get_object_or_404(Sezione,pk=pk)
    discussioni = Discussione.objects.filter(sezione_appartenenza=sezione).order_by("-data")
    context = {'sezione':sezione,'discussioni':discussioni}
    return render(request,'sezione.html',context)

@login_required
def crea_discussione_form(request,pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    if request.method == 'POST':
        form = CreaDiscussioneForm(request.POST)
        if form.is_valid():
            discussione = form.save(commit=False)
            discussione.sezione_appartenenza = sezione
            discussione.autore = request.user
            discussione.save()
            url = sezione.get_absolute_url()
            return HttpResponseRedirect(url)
    else:
        form = CreaDiscussioneForm()
    context = {'sezione':sezione,'form':form}
    return render(request,'crea-discussione.html',context)

def discussione(request,pk):
    discussione = get_object_or_404(Discussione,pk=pk)
    posts = Post.objects.filter(discussione_appartenenza=discussione)
    paginator = Paginator(posts,5)
    numero_pagina = request.GET.get('pagina')
    page_obj = paginator.get_page(numero_pagina)
    form_risposta = CreaPostForm()
    context = {'discussione':discussione,'posts':page_obj,'form':form_risposta}
    return render(request,'discussione.html',context)




def form_post_risposta(request,pk):
    discussione = get_object_or_404(Discussione, pk=pk)
    if request.method == 'POST':
        form = CreaPostForm(request.POST)
        if form.is_valid():
            risposta = form.save(commit=False)
            risposta.discussione_appartenenza = discussione
            risposta.autore = request.user
            risposta.save()
            url = discussione.get_absolute_url()
            numero_di_pagine = discussione.get_number_of_pages()
            if numero_di_pagine > 1:
                success_url = str(url) + '?pagina=' + str(numero_di_pagine)
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(url)
    else:
        return HttpResponseBadRequest


def funzione_cerca(request):
    if "q" in request.GET:
        query = request.GET.get("q")
        if len(query) == 0:
            return HttpResponseRedirect('/')
        else:
            users = User.objects.filter(username__icontains=query)
            discussioni = Discussione.objects.filter(titolo__icontains=query)
            posts = Post.objects.filter(contenuto__icontains=query)
            context = {'users':users,'discussioni':discussioni,'posts':posts}
            return render(request,'funzione-cerca.html',context)



class DeletePost(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'delete-post.html'

    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(autore_id=self.request.user.id)


#DELETE VIEW