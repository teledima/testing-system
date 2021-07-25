from django.urls import path
from tests import views

urlpatterns = [
    path('', views.testing, name='testing'),
    path('action', views.test_action, name='action')
]
