from archive.models import Problem, Submission, TestInstance, Test, Comparator
from django_q.tasks import async, result
import os
from . import helper
from subprocess import Popen, PIPE
import traceback
import base64


def judge_submission(submission_id):
	submission = Submission.objects.get(pk=submission_id)
	print("judging: {}".format(submission_id))
	
	for test_inst in submission.tests.all():
		async('judge.judge.evaluate_test',test_inst.id)




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
		judge_code = ""

		if problem.no_io:
			judge_code = problem.judge.read().decode()

		
		if not problem.no_io:
			judge_out, j_code = helper.run(judge_sol,problem.time_limit,input_data)
		else:
			judge_out, j_code = helper.run_with_judge(judge_code,judge_sol,problem.time_limit,input_data)

		if j_code != 'ok':
			make_verdict(test_inst,'EE',"The judge solution failed.\n"+judge_out)
			return

		if not problem.no_io:
			user_out, u_code = helper.run(user_sol, problem.time_limit, input_data)
		else:
			user_out, u_code = helper.run_with_judge(judge_code,user_sol,problem.time_limit,input_data)
			
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
			make_verdict(test_inst,'AC','Your solution passed this test correctly.')
		else:
			make_verdict(test_inst,'WA','Your solution finished, but it got the wrong solution.')

	except Exception as e:
		make_verdict(test_inst, 'EE', 'Something has failed, please contact the administrator.\n'+ traceback.format_exc())


def make_verdict(test_inst, verdict, details):
	test_inst.verdict = verdict
	test_inst.details = details
	test_inst.evaluated = True
	test_inst.save()



def compare(comparator, input_data, judge_out, user_out):
	source = comparator.file.read().decode()

	input_data = base64.b64encode(input_data.encode()).decode()
	judge_out = base64.b64encode(judge_out.encode()).decode()
	user_out = base64.b64encode(user_out.encode()).decode()

	data = input_data+'\n'+judge_out+'\n'+user_out
	p = Popen(['python3', '-c', source],
              stdout=PIPE, stdin=PIPE, stderr=PIPE)

	out, err = p.communicate(data.encode())
       
	print('Err:', err.decode())
	if err.decode()!='':
		raise RuntimeError()

	return int(out.decode())












