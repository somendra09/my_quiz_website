from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import Result
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def quiz_view(request):
    if request.method == 'POST':
        score = 0
        for i in range(10):
            selected = request.POST.get(f'q{i}')
            correct = request.POST.get(f'correct{i}')
            if selected == correct:
                score += 1
        Result.objects.create(user=request.user, score=score)
        return render(request, 'result.html', {'score': score})
    
    res = requests.get("https://opentdb.com/api.php?amount=10&type=multiple")
    data = res.json()['results']
    for q in data:
        q['answers'] = [q['correct_answer']] + q['incorrect_answers']
        import random
        random.shuffle(q['answers'])

    return render(request, 'quiz.html', {'data': data})

