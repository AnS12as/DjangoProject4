from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .forms import CustomUserCreationForm


class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_mail(
            'Подтверждение регистрации',
            'Спасибо за регистрацию.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'registration/password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if user:
            new_password = get_random_string(length=8)
            user.password = make_password(new_password)
            user.save()
            send_mail(
                'Сброс пароля',
                f'Ваш новый пароль: {new_password}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        return redirect('login')
