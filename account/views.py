from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login



def signup_view(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			user = form.save()
			auth_login(request, user)

			return redirect('home')
	else:
		form = SignUpForm()

	return render(request, 'account/signup.html', {'form': form})

def profile_view(request, username):
	user = None

	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		raise Http404

	return render(request,'account/profile.html', {'user_profile': user} )