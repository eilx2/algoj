from django.shortcuts import render
from .forms import SignUpForm




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