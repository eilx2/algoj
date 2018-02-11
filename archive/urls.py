from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.archive_view, name='archive'),
	path('<code>', views.problem_view, name='problem'),
	path('<code>/submissions', views.submissions_view, name='submissions'),
]