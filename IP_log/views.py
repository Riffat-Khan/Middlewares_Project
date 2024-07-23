from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from .enum import RoleChoice


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[(role.value, role.name) for role in RoleChoice], required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        profile = Profile(user=user, role=self.cleaned_data['role'], count=0)
        if commit:
            profile.save()
        return user


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
class LoggingIP(View):
    def get(self, request):
        ip_address = getattr(request, 'ip_address', 'Unknown')
        req_time = getattr(request, 'request_time', 'Unknown')
        access_count = getattr(request, 'access_count', 'Unknown')

        context = {
            'ip_address': ip_address,
            'req_time': req_time,
            'access_count': access_count,
        }
        return render(request, 'home.html', context)
    
class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form=None)

    def get_success_url(self):
        return reverse_lazy('logging_data') 

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Credentials')
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))
    
        