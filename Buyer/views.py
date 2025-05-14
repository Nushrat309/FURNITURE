from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import RegistrationForm  # Make sure this exists

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')


def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))
