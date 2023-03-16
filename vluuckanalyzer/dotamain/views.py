from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .utils import *
from .forms import *

# menu = [{'title': 'Про сайт', 'url_name': 'about'}, 
#         {'title': 'Додати статтю', 'url_name': 'add_page'}, 
#         {'title': 'Фідбек', 'url_name': 'contact'}, 
# ]

# Create your views here.

class DotamainHome(DataMixin, ListView):
    paginate_by = 7
    model = Match #назва моделі даних
    template_name = 'dotamain/indexblock.html'
    context_object_name = 'posts' #для перебору записів в базі даних
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Головна сторінка")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Match.objects.filter(is_published=True)


# def index(request): #HTTP request
#     posts = Match.objects.all()

#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Головна сторінка',
#         'cat_selected': 0
#     }
#     return render(request, 'dotamain/indexblock.html', context=context)
    
def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        

    return render(request, 'dotamain/contact.html', {'form': form, 'menu': menu, 'title': 'Фідбек'})

# def contact(request):
#     return HttpResponse("Зворотній зв'язок")





# def login(request):
#     return render(request, 'dotamain/login.html', {'menu': menu, 'title': 'Авторизація'})

def about(request): #HTTP request
    return render(request, 'dotamain/aboutblock.html', {'menu': menu, 'title': 'Про сайт'})

def somepage(request, matchid):
    if (request.GET):
        print(request.GET)
        
    return HttpResponse(f"<ul>somepage</ul><p>{matchid}</p>")

def archive(request, year):
    if int(year) > 2023:
        raise Http404()

    if int(year) == 2023:
        return redirect('home', permanent = True)

    return HttpResponse(f'<h1>Архів по рокам</h1><p>{year}</p>')

class ShowPost(DataMixin, DetailView):
    model = Match
    template_name = 'dotamain/post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post' #в цю змінну поміщаються дані з моделі бд

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Головна сторінка")
        return dict(list(context.items()) + list(c_def.items()))

        
# def show_post(request, post_id):
#     post = get_object_or_404(Match, pk=post_id)

#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }

#     return render(request, 'dotamain/post.html', context=context)

class DotamainCategory(DataMixin, ListView):
    paginate_by = 2
    model = Match
    template_name = 'dotamain/indexblock.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Match.objects.filter(cat__pk=self.kwargs['cat_id'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія - ' + str(context['posts'][0].cat), cat_selected = context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
#     posts = Match.objects.filter(cat_id=cat_id)

#     if len(posts) == 0:
#         raise Http404
        
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'По рубрикам',
#         'cat_selected': cat_id
#     }
#     return render(request, 'dotamain/indexblock.html', context=context)
    

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Цієї сторінки не знайдено</h1>')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'dotamain/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регістрація')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'dotamain/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')