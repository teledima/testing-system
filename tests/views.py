from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from tests.models import TestInfo, QuestionInfo, TestingResults, QuestionAnswer, QuestionAnswerUser, HtmlBlocks
import datetime
from enum import Enum
from django.db import connection


class QuestionType(Enum):
    ONE = 3
    SEVERAL = 4
    MANUAL = 6


@cache_control(must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def testing(request):
    if 'question' not in request.session:
        return render(request, 'tests/start_page.html')
    return render(request, 'tests/test.html', context={
        'question': request.session['question'] if 'question' in request.session else None,
        'answers': request.session['answers'] if 'answers' in request.session else None,
        'time_to_solve': request.session['time_to_solve'] if 'time_to_solve' in request.session else None,
        'has_prev': request.session['has_prev'] if 'has_prev' in request.session else None,
        'has_next': request.session['has_next'] if 'has_next' in request.session else None,
        'temp_answers': request.session['temp_answers'].get(str(request.session['question']['id'])) if 'temp_answers' in request.session and 'question' in request.session else None
    })


@cache_control(must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def test_action(request):
    action_type = request.POST.get('action-type')
    if action_type == 'start':
        request.session.clear()
        request.session.setdefault('temp_answers', dict())
        request.session['test-id'] = request.POST.get('test-id')
    test = TestInfo.objects.get(pk=request.session['test-id'])
    if action_type == 'start':
        question = test.questions.first()
    elif action_type == 'next':
        temp_save(request)
        question = test.questions.filter(ord__gt=request.session['ord']).first()
    elif action_type == 'prev':
        temp_save(request)
        question = test.questions.filter(ord__lt=request.session['ord']).last()
    elif action_type == 'finish':
        temp_save(request)
        request.session['result-id'] = finish_testing(request)
        request.session.pop('question', None)
        request.session.pop('answers', None)
        request.session.pop('has_next', None)
        request.session.pop('has_prev', None)
        request.session.pop('time_to_solve', None)
        return redirect('tests:result')

    request.session['ord'] = question.ord
    request.session['question'] = dict(id=question.id, question_text=question.question_text, question_type=question.question_type.type_name)
    if question.question_type.type_name in [question_type.name for question_type in QuestionType]:
        request.session['answers'] = [
            question.question_type.html_block.html_block.format(name=f"ANSWER-{question.id}-{question.question_type.type_name}",
                                                                id=answer.id,
                                                                text=answer.answer_text)
            for answer
            in question.answers]

    request.session['time_to_solve'] = test.time_to_solve if action_type == 'start' else int(
        request.POST.get('available-time')) + 1
    request.session['has_prev'] = True if test.questioninfo_set.all().filter(
        ord__lt=question.ord).last() is not None else False
    request.session['has_next'] = True if test.questioninfo_set.all().filter(
        ord__gt=question.ord).first() is not None else False
    return redirect('tests:testing')


def testing_result(request):
    count_correct, count_incorrect, ball = get_results(request.session['result-id'])
    result_block = HtmlBlocks.objects.get(pk=4).html_block.format(count_correct=count_correct,
                                                                  count_incorrect=count_incorrect,
                                                                  ball=ball)

    return render(request, 'tests/testing_result.html', context={"result_block": result_block})


def temp_save(request):
    selected_answer = [request.POST.getlist(key) for key in request.POST if 'ANSWER' in key]
    temp_answers = request.session['temp_answers']
    if len(selected_answer) == 0:
        if str(request.session['question']['id']) in temp_answers:
            temp_answers[str(request.session['question']['id'])] = None
        return
    assert len(selected_answer) == 1
    temp_answers[str(request.session['question']['id'])] = selected_answer[0]


def finish_testing(request):
    result = TestingResults(test=TestInfo.objects.get(pk=request.session['test-id']),
                            user=request.user,
                            testing_date=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    result.save()

    for question_id in request.session['temp_answers']:
        temp_question = QuestionInfo.objects.get(pk=question_id)
        if temp_question.question_type.type_name == 'MANUAL':
            QuestionAnswerUser(result=result,
                               question_answer=QuestionAnswer.objects.get(pk=request.session['temp_answers'][question_id]),
                               entered_text=request.session['temp_answers'][question_id]).save()
        else:
            for selected_answer in request.session['temp_answers'][question_id]:
                QuestionAnswerUser(result=result,
                                   question_answer=QuestionAnswer.objects.get(pk=selected_answer),
                                   entered_text=None).save()

    return result.id


def get_results(result_id):
    with connection.cursor() as cursor:
        cursor.execute('select count_correct, count_incorrect, ball '
                       'from get_results(p_result_id => {p_result_id})'.format(p_result_id=result_id))
        count_correct, count_incorrect, ball = cursor.fetchone()
    return count_correct, count_incorrect, ball
