from datetime import datetime
import logging

logging.basicConfig(filename='log_data', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)

class logging_time:
  def __init__(self, get_response):
    self.get_response = get_response
    
  def __call__(self, request):
    req_time = datetime.now().time()
    request.request_time = req_time
    
    logger.info(f'{req_time}')
    
    response = self.get_response(request)
    return response
    