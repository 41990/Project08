
from django.urls import path
from .views import PrivilegeView

urlpatterns = [
    path('home', PrivilegeView.as_view(), name='home'),
]