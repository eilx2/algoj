from django.shortcuts import render, HttpResponse
from .models import Problem, Submission, TestInstance
from django.http import Http404
from .forms import SubmitSolForm
from django_q.tasks import async, result
from django.core import serializers
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from datetime import datetime,timezone

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
		cr_date = datetime.now(timezone.utc)
		last_sub = request.user.profile.last_submission
		

		dif = (cr_date-last_sub).total_seconds()
		context['source'] = request.POST['source']
		

		if dif>=30:

			context['message']='Your solution was submitted successfuly! Go to the "Submissions" page.'
			context['msg_type']='success'


			print('Submitted solution:',request.POST['source'])
			
			submission = Submission.objects.create(source=request.POST['source'], problem = problem, user = request.user)

			for test in submission.problem.tests.all():
				test_instance = TestInstance.objects.create(submission=submission, test=test)

			request.user.profile.last_submission = datetime.now(timezone.utc)
			request.user.profile.save()

			async('judge.judge.judge_submission',submission.id)
		else:
			context['message'] = 'You must wait at least 30 seconds before submitting another solution.'
			context['msg_type'] = 'danger'

	if request.user.is_authenticated:
		submissions = Submission.objects.filter(user=request.user, problem=problem)

		if submissions:
			submission = submissions.latest('date', 'time')
			if not 'source' in context:
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



