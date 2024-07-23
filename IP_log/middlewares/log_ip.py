import logging
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.cache import cache
from ..enum import RoleChoice
from ..models import Profile

class MiddlewareForLoggingData:
  def __init__(self, get_response):
    self.get_response = get_response
    self.logger = logging.getLogger(__name__)
    
  def __call__(self, request):
    if request.path == '/ip_logging/' :
      req_header = request.META
      req_time = datetime.now().time()
      
      request.request_time = req_time
      self.logger.info(req_time)
      
      x_forwarded_for = req_header.get('HTTP_X_FORWARDED_FOR')
      if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
      else:
        ip_addr = request.META.get('REMOTE_ADDR')
        
      request.ip_address = ip_addr
      request.request_time = timezone.now().isoformat()
      self.logger.info(ip_addr)

      if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        last_access_time = profile.last_access_time

        current_count = profile.count
        req_datetime = timezone.now()
        if last_access_time and (req_datetime - last_access_time) > timedelta(minutes=1):
          current_count = 0

        new_count = current_count + 1
        profile.count = new_count
        profile.last_access_time = req_datetime
        profile.save()

        if profile.role == RoleChoice.GOLD.value:
          if new_count > 10:
            return HttpResponse('Too many requests', status=429)
        elif profile.role == RoleChoice.SILVER.value:
          if new_count > 5:
            return HttpResponse('Too many requests', status=429)
        elif profile.role == RoleChoice.BRONZE.value:
          if new_count > 2:
            return HttpResponse('Too many requests', status=429)
      else:
        return HttpResponse('Too many requests', status=429)
      
      request.access_count = new_count
      self.logger.info(new_count)
      
      response = self.get_response(request)
      return response

    else:
      response = self.get_response(request)
      return response