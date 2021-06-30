from django.urls import path, include
from tests import views

urlpatterns = [
    path('', views.start_test, name='start_test')
]
