from django.shortcuts import render
from django.core import serializers
from tests.models import TestInfo


def start_page(request):
    context = {'all_tests': serializers.serialize('python', TestInfo.objects.all()),
               'columns': [field.verbose_name for field in TestInfo._meta.get_fields()
                           if hasattr(field, 'verbose_name') and field.verbose_name != ''],
               'test_string': 'test'}
    return render(request, 'tests/start_page.html', context=context)


def start_test(request):
    first_question = TestInfo(request.POST.get('test-id')).questions.first()
    answers = [first_question.question_type.html_block.format(name=first_question.question_type.type_name,
                                                              id=answer.id,
                                                              text=answer.answer_text)
               for answer
               in first_question.questionanswer_set.all()]
    return render(request, 'tests/test.html', context={'question': first_question, 'answers': answers})
