from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class TestInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='')
    test_name = models.CharField(max_length=255, verbose_name='Название теста')
    description = models.CharField(max_length=4000, verbose_name='Описание теста', null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                                verbose_name='Составитель теста', to_field='username')
    time_to_solve = models.PositiveIntegerField(verbose_name='Время для решения', null=True)
    questions = models.ManyToManyField(to='QuestionInfo', through='TestQuestion')

    class Meta:
        db_table = 'tests_info'
        verbose_name = 'Test Info'
        verbose_name_plural = 'Tests Info'


class QuestionInfo(models.Model):
    id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=4000, verbose_name='Текст вопроса')
    question_type = models.ForeignKey(to='QuestionType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'questions_info'
        verbose_name = 'Question info'
        verbose_name_plural = 'Questions info'


class QuestionType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, verbose_name=_('Type name'))
    html_block = models.CharField(max_length=4000, verbose_name=_('Html code block for type'), default='')

    class Meta:
        db_table = 'question_types'
        verbose_name = 'Question Type'
        verbose_name_plural = 'Question types'


class TestQuestion(models.Model):
    test = models.ForeignKey(to=TestInfo, on_delete=models.CASCADE)
    question = models.ForeignKey(to=QuestionInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tests_questions'
        verbose_name = 'Question in test'
        verbose_name_plural = 'Questions in test'


class QuestionAnswer(models.Model):
    question = models.ForeignKey(to=QuestionInfo, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255, verbose_name='Вариант ответа')
    is_correct = models.PositiveIntegerField(verbose_name='Правильность ответа')

    class Meta:
        db_table = 'questions_answers'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
