from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from notes import views as notes_views
from notes.views import WelcomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WelcomeView.as_view(), name='home'),
    path('welcome/', notes_views.WelcomeView.as_view(), name='welcome'),
    path('notes/', include('notes.urls')),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),
    path('register/', notes_views.register, name='register'),

    # Включение URL-адресов приложения notes
    path('notes/', include('notes.urls')),

    # Сброс пароля
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete')
]