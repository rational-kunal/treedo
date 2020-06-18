from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import render, redirect


def sign_up(request):
    context = {}
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('label_index')
    context['form'] = form
    return render(request, 'registration/sign_up.html', context)
