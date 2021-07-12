from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tests.models import TestInfo


@login_required(login_url='/login/')
def start_test(request):
    test = TestInfo.objects.get(pk=request.POST.get('test-id'))
    first_question = test.questions.first()
    answers = [first_question.question_type.html_block.format(name=first_question.question_type.type_name,
                                                              id=answer.id,
                                                              text=answer.answer_text)
               for answer
               in first_question.questionanswer_set.all()]
    return render(request, 'tests/test.html', context={'question': first_question, 'answers': answers,
                                                       'time_to_solve': test.time_to_solve})
