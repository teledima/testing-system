from django.shortcuts import render, HttpResponse
from django.core import serializers
from tests.models import TestInfo


def start_page(request):
    context = {'all_tests': serializers.serialize('python', TestInfo.objects.all()),
               'columns': [field.verbose_name for field in TestInfo._meta.get_fields()
                           if field.verbose_name != ''],
               'test_string': 'test'}
    return render(request, 'tests/start_page.html', context=context)


def start_test(request):
    return render(request, 'tests/test.html', context={'id': request.POST.get('test-id')})
