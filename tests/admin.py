from django.contrib import admin
from .models import TestInfo, TestQuestion, QuestionAnswer, QuestionInfo

admin.site.register(TestInfo)
admin.site.register(TestQuestion)
admin.site.register(QuestionAnswer)
admin.site.register(QuestionInfo)
