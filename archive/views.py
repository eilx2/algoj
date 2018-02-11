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

		context['message']='Your solution was submitted successfuly!'

		print('Submitted solution:',request.POST['source'])
		submission = Submission.objects.create(source=request.POST['source'], problem = problem, user = request.user)

		async('judge.judge.judge_submission',submission.id)

		return render(request,"problem.html",context=context)


	return render(request,"problem.html",context=context)




def submissions_view(request, code):
	problem = None
	context = {}
	user = request.user

	try:
		problem = Problem.objects.get(code=code)
		context['problem'] = problem
	except Problem.DoesNotExist:
		raise Http404

	if not request.user.is_authenticated:
		return render(request,"submissions.html",context=context)

	submissions = problem.submissions.filter(user=user)

	context['submissions']=submissions

	return render(request,"submissions.html", context=context)
