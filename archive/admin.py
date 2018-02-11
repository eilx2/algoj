from django.contrib import admin
from .models import Problem, Submission, Test, TestInstance, Tag, Profile, Comparator

# Register your models here.

admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Test)
admin.site.register(TestInstance)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Comparator)