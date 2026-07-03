from django.shortcuts import render, redirect
from .forms import BMIForm

# Create your views here.


def homepage(request):
    return render(request, 'calculator/homepage.html')

def calculator(request):
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            request.session['bmi'] = round(weight / (height ** 2), 2)
            # context = {'bmi': request.session['bmi'], 'form': form}
            if request.session['bmi'] < 18.5:
                request.session['message'] = 'You are underweight.'
            elif 18.5 <= request.session['bmi'] < 25:
                request.session['message'] = 'You have a normal weight.'
            elif 25 <= request.session['bmi'] < 30:
                request.session['message'] = 'You are overweight.'
            else:
                request.session['message'] = 'You are obese.'
            return redirect('calculator:calculator')
    else:
        form = BMIForm()

    bmi = request.session.pop('bmi', None)
    message = request.session.pop('message', None)
    context = {'form': form, 'bmi': bmi, 'message': message}

    return render(request, 'calculator/calculator.html', context)