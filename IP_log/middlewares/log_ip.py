import logging

logging.basicConfig(filename='log_data', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)

class logging_ip:
  def __init__(self, get_response):
    self.get_response = get_response
    
  def __call__(self, request):
    req_header = request.META
    
    x_forwarded_for = req_header.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
      ip_addr = x_forwarded_for.split(',')[0]
    else:
      ip_addr = request.META.get('REMOTE_ADDR')
      
    request.ip_address = ip_addr
    logger.info(f"{ip_addr}")

    response = self.get_response(request)
    return response
    