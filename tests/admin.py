from django.contrib import admin
from .models import TestInfo, QuestionAnswer, QuestionInfo

admin.site.register(TestInfo)
admin.site.register(QuestionAnswer)
admin.site.register(QuestionInfo)
