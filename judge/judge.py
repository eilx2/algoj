from archive.models import Problem, Submission, TestInstance, Test, Comparator
from django_q.tasks import async, result
import os
from . import helper
from subprocess import Popen, PIPE
import traceback

def judge_submission(submission_id):
	submission = Submission.objects.get(pk=submission_id)
	print("judging: {}".format(submission_id))
	

	for test in submission.problem.tests.all():
		test_instance = TestInstance.objects.create(submission=submission, test=test)
		async('judge.judge.evaluate_test',test_instance.id)




def evaluate_test(test_instance_id):
	print('running:',test_instance_id)
	test_inst = TestInstance.objects.get(pk=test_instance_id)

	try:
		test=test_inst.test
		submission = test_inst.submission
		problem = submission.problem
		comparator = problem.comparator

		print('ok, got in')
		# get input data
		input_data = test.file.read().decode()

		judge_sol = problem.solution.read().decode()
		user_sol = submission.source

		
		judge_out, j_code = helper.run(judge_sol,problem.time_limit,input_data)

		if j_code != 'ok':
			make_verdict(test_inst,'EE',judge_out)
			return

		user_out, u_code = helper.run(user_sol, problem.time_limit, input_data)
		if u_code != 'ok':
			if u_code == 'tle':
				make_verdict(test_inst,'TLE','Your solution has passed over the time limit.')
			elif u_code =='user_err':
				make_verdict(test_inst,'RE',user_out)
			else:
				make_verdict(test_inst,'EE',user_out)

			return


		verdict = compare(comparator,input_data,judge_out,user_out)

		if verdict==1:
			make_verdict(test_inst,'AC','')
		else:
			make_verdict(test_inst,'WA','')

	except Exception as e:
		make_verdict(test_inst, 'EE', 'Something has failed, please contact the administrator.\n'+ traceback.format_exc())


def make_verdict(test_inst, verdict, details):
	test_inst.verdict = verdict
	test_inst.details = details
	test_inst.evaluated = True
	test_inst.save()

def compare(comparator, input_data, judge_out, user_out):
	source = comparator.file.read().decode()

	input_data = helper.remove_newlines(input_data)
	judge_out = helper.remove_newlines(judge_out)
	user_out = helper.remove_newlines(user_out)

	p = Popen(['python3', '-c', source]
              stdout=PIPE, stdin=PIPE, stderr=PIPE)

	out, err = p.communicate(input_data+'\n'+judge_out+'\n'+user_out+'\n')

	if err.decode()!='':
		raise RuntimeException()

	return int(out.decode())












