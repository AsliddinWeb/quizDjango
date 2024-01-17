from django.shortcuts import render, redirect, HttpResponse

import random

from .models import Question, Choice
from .forms import NameForm

def home_page(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            # Save the user's name in the session for later use
            request.session['name'] = form.cleaned_data['name']
            return redirect('question_list')
    else:
        form = NameForm()

    return render(request, 'home-page.html', {'form': form})


def question_list(request):
    name = request.session.get('name', 'Mehmon')

    if request.method == 'POST':
        selected_choices = {}
        correct_answers = 0

        for question in Question.objects.all():
            choice_id = request.POST.get(f'choice{question.id}')

            if choice_id:
                selected_choices[question.id] = int(choice_id)
                choice = Choice.objects.get(id=choice_id)
                if choice.is_correct:
                    correct_answers += 1

        request.session['results'] = {
            'selected_choices': selected_choices,
            'correct_answers': correct_answers,
            'total_questions': Question.objects.count(),
        }

        return redirect('result_view')

    all_questions = Question.objects.all()
    selected_questions = random.sample(list(all_questions), min(20, len(all_questions)))

    ctx = {
        'questions': selected_questions,
        'name': name
    }
    return render(request, 'question_list.html', ctx)

# result_view view
def result_view(request):
    results = request.session.get('results')

    if not results:
        return redirect('question_list')

    selected_choices = results.get('selected_choices')
    correct_answers = results.get('correct_answers')
    total_questions = results.get('total_questions')

    if not selected_choices or correct_answers is None or total_questions is None:
        return HttpResponse("Invalid data in the session.")

    details = []

    for question_id, choice_id in selected_choices.items():
        question = Question.objects.get(id=question_id)
        choice = Choice.objects.get(id=choice_id)

        details.append({
            'question_text': question.question_text,
            'your_answer': choice.choice_text,
            'is_correct': choice.is_correct,
            'correct_answer': next((c.choice_text for c in question.choices.all() if c.is_correct), None),
        })

    ctx = {
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'details': details,
    }

    # request.session.pop('results', None)

    return render(request, 'result.html', ctx)

