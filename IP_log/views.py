from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.views import LoginView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UserRole

class LoggingIP(View):
  
  @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)
  
  def get(self, request):
    ip_address = getattr(request, 'ip_address', 'Unknown')
    req_time = getattr(request, 'request_time', 'Unknown')

    ip_and_time = f'{ip_address}, {req_time}'
    
    return HttpResponse(ip_and_time)
  
class home(TemplateView):
  @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)
  
  template_name = 'home.html'
    
  
  
class LoginView(LoginView):
  @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)
  
  def get_success_url(self):
    return 
  
  def form_invalid(self, form):
    messages.error(self.request, 'Invalid Credentials')
    """If the form is invalid, render the invalid form."""
    return self.render_to_response(self.get_context_data(form=form))
  
  
  template_name = 'login.html'
  
  
class RoleBasedAccess(ListView):
  model = UserRole
  
  def head(self, *args, **kwargs):
    user_role = UserRole.get('role')
    # if not user.is_au
    if user_role == 'gold':
      rate = '10/m'
    if user_role == 'silver':
      rate = '5/m'
    if user_role == 'bronze':
      rate = '2/m'
    if user_role == 'unauthenticated':
      rate = '1/m'

    return rate
              
  # @method_decorator(ratelimit(key='ip', rate=rate, block=True))
  # def dispatch(self, *args, **kwargs):
  #   return super().dispatch(*args, **kwargs)
  
  
  

    
