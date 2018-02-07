from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def get_score(self, problem):
		score = 0
		submissions = Submission.objects.filter(problem__iexact=problem, user_iexact = self.user)

		for submission in submissions:
			score = max(score, submission.get_score())

		return score

	def has_submitted(self, problem):
		submissions = Submission.objects.filter(problem__iexact=problem, user_iexact = self.user)

		return len(submissions)>0


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tag(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

def grader_dir(self, filename):
	return 'problems/'+self.code+'/grader/'+'grader.py'

def tests_dir(self, filename):
	return 'problems/'+self.problem.code+'/tests/'+str(filename)


class Problem(models.Model):
	name = models.CharField(max_length=40, unique=True)
	code = models.CharField(max_length=40, unique=True)

	statement = models.TextField()
	time_limit = models.IntegerField(default=2000)
	memory_limit = models.IntegerField(default=256)

	date = models.DateTimeField()

	grader = models.FileField(upload_to=grader_dir, null='true')

	tags = models.ManyToManyField(Tag)

	class Meta:
		ordering = ["date", "name"]

	def nr_of_tests(self):
		return self.tests.count()

	def __str__(self):
		return self.name



class Submission(models.Model):
	date = models.DateField(default=datetime.date.today)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True, related_name="submissions")
	source = models.TextField()

	def __str__(self):
		return self.problem.name+'-'+str(self.user)+'-'+str(self.date)

	def get_score(self):
		tests = self.tests.all()
		score = 0

		for test in tests:
			if test.verdict == 'AC':
				score+=1

		return score

	def is_evaluated(self):
		tests = self.tests.all()

		for test in tests:
			if not test.evaluated:
				return False

		return True

	


class Test(models.Model):
	file = models.FileField(upload_to=tests_dir, default=None)
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="tests")


	def __str__(self):
		return self.problem.name+"-"+str(self.id)



class TestInstance(models.Model):
	
	test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="tests")
	evaluated = models.BooleanField(default=False)

	VERDICTS = [ ('AC', 'Accepted'),
				 ('TLE', 'Time Limit Exceeded'),
				 ('MLE', 'Memory Limit Exceeded'),
				 ('RE', 'Runtime Error'),
				 ('EE', 'Evaluation Error'),
				 ('RNG', 'Running...'),
	]

	verdict = models.CharField(max_length=5, choices=VERDICTS, default='RNG')

	time = models.IntegerField(default=0)
	memory = models.IntegerField(default=0)



