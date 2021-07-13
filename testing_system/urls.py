"""testing_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.core import serializers
from django.shortcuts import render
from tests import models


def default(request):
    return render(request, 'default.html')


@login_required(login_url='/login/')
def home(request):
    context = {'all_tests': serializers.serialize('python', models.TestInfo.objects.all()),
               'columns': [field.verbose_name for field in models.TestInfo._meta.get_fields()
                           if hasattr(field, 'verbose_name') and field.verbose_name != ''],
               'test_string': 'test'}
    return render(request, 'tests/start_page.html', context=context)


urlpatterns = [
    path('', default, name='default'),
    path('home/', home, name='start_page'),
    path('admin/', admin.site.urls),
    path('tests/', include(('tests.urls', 'tests'), namespace='tests')),
    path('login/', LoginView.as_view(), name='login')
]
