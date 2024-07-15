from django.urls import path
from . import views

urlpatterns = [
  path('ip_logging/', views.LoggingIP.as_view(), name='logging_data'),
  # path('home/', views.home.as_view()),
  path('login/', views.LoginView.as_view(), name='login'),
  path('login/None', views.home.as_view())
]