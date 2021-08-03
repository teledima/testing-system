from django.shortcuts import render, redirect
from tests.models import TestInfo


def testing(request):
    return render(request, 'tests/test.html', context={
        'question': request.session['question'],
        'answers': request.session['answers'],
        'time_to_solve': request.session['time_to_solve'],
        'has_prev': request.session['has_prev'],
        'has_next': request.session['has_next'],
        'temp_answers': request.session['temp_answers'].get(str(request.session['question']['id'])) if 'temp_answers' in request.session else None
    })


def test_action(request):
    def temp_save():
        selected_answer = [request.POST.getlist(key) for key in request.POST if 'ANSWER' in key]
        temp_answers = request.session['temp_answers']
        if len(selected_answer) == 0:
            if str(request.session['question']['id']) in temp_answers:
                temp_answers[str(request.session['question']['id'])] = None
            return
        assert len(selected_answer) == 1
        request.session.setdefault('temp_answers', dict())
        temp_answers[str(request.session['question']['id'])] = selected_answer[0]

    action_type = request.POST.get('action-type')
    if action_type == 'start':
        request.session.clear()
        request.session['test-id'] = request.POST.get('test-id')
    test = TestInfo.objects.get(pk=request.session['test-id'])
    if action_type == 'start':
        question = test.questioninfo_set.first()
    elif action_type == 'next':
        temp_save()
        question = test.questioninfo_set.all().filter(ord__gt=request.session['ord']).first()
    elif action_type == 'prev':
        temp_save()
        question = test.questioninfo_set.all().filter(ord__lt=request.session['ord']).last()

    request.session['ord'] = question.ord
    request.session['question'] = dict(id=question.id, question_text=question.question_text, question_type=question.question_type.type_name)
    if question.question_type.type_name in ['SEVERAL', 'ONE', 'MANUAL']:
        request.session['answers'] = [
            question.question_type.html_block.format(name=f"ANSWER-{question.id}-{question.question_type.type_name}",
                                                     id=answer.id,
                                                     text=answer.answer_text)
            for answer
            in question.questionanswer_set.all()]

    request.session['time_to_solve'] = test.time_to_solve if action_type == 'start' else int(
        request.POST.get('available-time')) + 1
    request.session['has_prev'] = True if test.questioninfo_set.all().filter(
        ord__lt=question.ord).last() is not None else False
    request.session['has_next'] = True if test.questioninfo_set.all().filter(
        ord__gt=question.ord).first() is not None else False
    return redirect('tests:testing')
