from django.db import models
from django.contrib.auth import get_user_model


class TestInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='')
    test_name = models.CharField(max_length=255, verbose_name='Название теста')
    description = models.CharField(max_length=4000, verbose_name='Описание теста', null=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                                verbose_name='Составитель теста', to_field='username')
    time_to_solve = models.PositiveIntegerField(verbose_name='Время для решения', null=True)

    class Meta:
        db_table = 'tests_info'
        verbose_name = 'Test Info'
        verbose_name_plural = 'Tests Info'
