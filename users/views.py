from django.shortcuts import render, redirect
from users.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView
# Create your views here.

class RegisterView(ListView, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request, **kwargs):
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        data = request.POST
        form = self.form_class(data=data)

        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                return redirect('/users/login/')
            else:
                form.add_error('password1', 'Пароли не совпадают!')
        return render(request, self.template_name, context={
            'form': form
        })



class LoginView(ListView, CreateView):
     template_name = 'users/login.html'
     form_class = LoginForm

     def get(self, request, **kwargs):
         context = {
             'form': self.form_class
         }
         return render(request, self.template_name, context=context)

     def post(self, request, **kwargs):
         data = request.POST
         form = self.form_class(data=data)

         if form.is_valid():
             user = authenticate(
                 username=form.cleaned_data.get('username'),
                 password=form.cleaned_data.get('password')
             )

             if user:
                 login(request, user)
                 return redirect('/products')
             else:
                 form.add_error('username', 'Пользователь не найден!')

         return render(request, self.template_name, context={
             'form': form
         })



class LogoutView(ListView):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('/products/')
