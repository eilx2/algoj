from django.contrib import admin
from .models import Problem, Submission, Test, TestInstance, Tag, Profile, Comparator, Example

# Register your models here.

class TestsInline(admin.TabularInline):
	model = Test
	extra = 0

class ExamplesInline(admin.TabularInline):
	model = Example
	extra = 0

class ProblemAdmin(admin.ModelAdmin):
	inlines = [
		ExamplesInline,
		TestsInline,
	]

class TestInstancesInline(admin.TabularInline):
	model = TestInstance
	extra = 0

class SubmissionAdmin(admin.ModelAdmin):
	inlines = [
		TestInstancesInline,
	]

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Test)
admin.site.register(TestInstance)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Comparator)
admin.site.register(Example)