from django.shortcuts import render, HttpResponse
from .models import Problem, Submission, TestInstance
from django.http import Http404
from .forms import SubmitSolForm
from django_q.tasks import async, result
from django.core import serializers
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def get_scores(user):
	scores = {}
	for problem in Problem.objects.all():
		scores[problem.code] = 0

	if user.is_anonymous:
		return scores
		
	submissions = Submission.objects.filter(user=user)
	for submission in submissions:
		problem = submission.problem
		score = submission.get_score()

		scores[problem.code]=max(scores[problem.code],score)
	
	return scores

# Create your views here.
def archive_view(request):
	problems = Problem.objects.all()
	

	return render(request,"archive.html",context={'problems' : problems, 'scores' : get_scores(request.user)})




def problem_view(request, code):
	context = {}
	problem = None

	try:
		problem = Problem.objects.get(code=code)
		context['problem'] = problem

	except Problem.DoesNotExist:
		raise Http404



	if request.method == 'POST' and request.user.is_authenticated:

		context['message']='Your solution was submitted successfuly! Go to the "Submissions" page.'

		print('Submitted solution:',request.POST['source'])
		submission = Submission.objects.create(source=request.POST['source'], problem = problem, user = request.user)

		async('judge.judge.judge_submission',submission.id)

	if request.user.is_authenticated:
		submissions = Submission.objects.filter(user=request.user, problem=problem)

		if submissions:
			submission = submissions.latest('date', 'time')
			context['source'] = submission.source



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

def parse_string(s):
	s=s.replace('\\r\\n','\n')
	s=s.replace('\\n','\n')
	return s

def submission_json_view(request, id):
	submission = None

	try:
		submission = Submission.objects.get(pk=id)
	except Submission.DoesNotExist:
		raise Http404

	submission.source = highlight(parse_string(submission.source),PythonLexer(),HtmlFormatter())
	tests = submission.tests.all()

	for test in tests:
		test.details = parse_string(test.details)

	data = '{}'
	if request.user == submission.user:
		data = '['+serializers.serialize('json',[submission,])+','+\
				serializers.serialize('json', tests)+']'

	return HttpResponse(data, content_type='application/json')



