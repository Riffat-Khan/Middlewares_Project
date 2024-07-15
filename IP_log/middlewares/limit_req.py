from django.http import HttpResponse
from django_ratelimit.decorators import Ratelimited

class LimitRequest:
  def __init__(self, get_response):
    self.get_response = get_response
    
  def __call__(self, request):   
    response = self.get_response(request)
    return response
    
  def process_exception(self, request, exception):
    if isinstance(exception, Ratelimited):
      return HttpResponse('Too many requests')
    
    return None