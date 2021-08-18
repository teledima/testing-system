from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class BlockTypes(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255, verbose_name='Тип блока')

    class Meta:
        db_table = 'block_types'


class HtmlBlocks(models.Model):
    id = models.AutoField(primary_key=True)
    html_block = models.CharField(max_length=4000, verbose_name='HTML код блока')
    block_type = models.ForeignKey(to=BlockTypes, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'html_blocks'


class TestInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='')
    test_name = models.CharField(max_length=255, verbose_name='Название теста')
    description = models.CharField(max_length=4000, verbose_name='Описание теста', null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                                verbose_name='Составитель теста', to_field='username')
    time_to_solve = models.PositiveIntegerField(verbose_name='Время для решения', null=True)
    max_ball = models.PositiveIntegerField(verbose_name='Максимальный балл за тест')

    @property
    def questions(self):
        return self.questioninfo_set.all()

    class Meta:
        db_table = 'tests_info'
        verbose_name = 'Test Info'
        verbose_name_plural = 'Tests Info'


class QuestionInfo(models.Model):
    id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=4000, verbose_name='Текст вопроса')
    question_type = models.ForeignKey(to='QuestionType', on_delete=models.CASCADE)
    test = models.ForeignKey(to='TestInfo', on_delete=models.CASCADE, null=False)
    ord = models.IntegerField(verbose_name=_('Order questions'), db_index=True, default=1)

    @property
    def answers(self):
        return self.questionanswer_set.all()

    class Meta:
        db_table = 'questions_info'
        ordering = ['ord']
        verbose_name = 'Question info'
        verbose_name_plural = 'Questions info'


class QuestionType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, verbose_name=_('Type name'))
    html_block = models.ForeignKey(to=HtmlBlocks, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'question_types'
        verbose_name = 'Question Type'
        verbose_name_plural = 'Question types'


class QuestionAnswer(models.Model):
    question = models.ForeignKey(to=QuestionInfo, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255, verbose_name='Вариант ответа')
    is_correct = models.PositiveIntegerField(null=True, verbose_name='Правильность ответа')

    class Meta:
        db_table = 'questions_answers'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class TestingResults(models.Model):
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey(to=TestInfo, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    testing_date = models.DateTimeField(verbose_name='Дата прохождения тестирования')

    class Meta:
        db_table = 'testing_results'


class QuestionAnswerUser(models.Model):
    result = models.ForeignKey(to=TestingResults, on_delete=models.DO_NOTHING)
    question_answer = models.ForeignKey(to=QuestionAnswer, on_delete=models.DO_NOTHING)
    entered_text = models.CharField(max_length=4000, null=True, verbose_name='Текст ответа (тип вопроса - MANUAL)')

    class Meta:
        db_table = 'question_answers_users'
        verbose_name = 'User answers'
        verbose_name_plural = 'Users answers'
