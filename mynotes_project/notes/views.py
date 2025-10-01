from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.db.models import Q
from .models import Note, Category
from .forms import NoteForm, CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.contrib import messages

@login_required
def home(request):
    return redirect('notes:note_list')

# Аутентификация
class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('notes:welcome')

@login_required
def custom_logout(request):
    logout(request)
    return redirect('notes:welcome')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes:note_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class WelcomeView(UserPassesTestMixin, TemplateView):
    template_name = 'notes/welcome.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('notes:note_list')

# Представления для заметок
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)

        # Фильтрация по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        # Поиск по тексту
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query))

        # Сортировка
        sort = self.request.GET.get('sort', '-updated_at')
        return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(owner=self.request.user)
        return context

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Исправлено с user на owner
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)  # Исправлено с user на owner

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note_list')

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)  # Исправлено с user на owner

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:note_list')

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)  # Исправлено с user на owner

# Представления для категорий
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'notes/category_form.html'
    success_url = reverse_lazy('notes:note_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'notes/category_confirm_delete.html'
    success_url = reverse_lazy('notes:note_list')

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Нельзя удалить категорию, так как она используется в заметках')
            return redirect('notes:note_list')