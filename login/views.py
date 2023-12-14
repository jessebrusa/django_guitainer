from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.views import View
from django import forms




class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = ['username', 'password', 'email']
    redirect_authenticated_user = True


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CustomRegisterView(View):
    template_name = 'base/register.html'
    redirect_authenticated_user = True

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('library')