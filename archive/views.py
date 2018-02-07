from django.shortcuts import render, HttpResponse
from .models import Problem, Submission
from django.http import Http404
from .forms import SubmitSolForm
from django_q.tasks import async, result

# Create your views here.
def archive_view(request):
	problems = Problem.objects.all()
	
	return render(request,"archive.html",context={'problems' : problems})



def problem_view(request, code):
	context = {}
	problem = None

	try:
		problem = Problem.objects.get(code=code)
		context['problem'] = problem

	except Problem.DoesNotExist:
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:
		form = SubmitSolForm(request.POST)
		context['form'] = form
		context['message']='Your solution was submitted successfuly!'

		submission = Submission.objects.create(source=form['source'], problem = problem, user = request.user)

		async('judge.judge.judge_submission',submission.id)

		if form.is_valid():
			return render(request,"problem.html",context=context)
	else:
		form = SubmitSolForm()
		context['form'] = form


	return render(request,"problem.html",context=context)
