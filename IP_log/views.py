from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

class LoggingIP(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'home.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['count'] = profile.count
        context['last_access_time'] = profile.last_access_time
        # context['ip_address'] = profile.ip_address
        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


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
    
        