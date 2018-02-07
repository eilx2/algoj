from archive.models import Problem, Submission, TestInstance, Test
from django_q.tasks import async, result

def judge_submission(submission_id):
	submission = Submission.objects.get(pk=submission_id)
	for test in submission.tests.all():
		test_instance = TestInstance.objects.create(submission=submission, test=test)
		async('judge.judge.evaluate_test',test_istance.id)


def evaluate_test(test_istance_id):
	pass