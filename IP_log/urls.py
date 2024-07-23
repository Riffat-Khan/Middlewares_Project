from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path("signup/", views.SignUpView.as_view(), name="signup"),
  path('ip_logging/', views.LoggingIP.as_view(), name='logging_data'),
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
]