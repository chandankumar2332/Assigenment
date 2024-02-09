from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required
from posts.models import CustomUser

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html', {'user': request.user})
@login_required
def doctor_dashboard(request):
    doctors = CustomUser.objects.filter(is_doctor=True)
    return render(request, 'doctor_dashboard.html', {'doctors': doctors})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_patient:
                    return redirect('patient_dashboard')
                elif user.is_doctor:
                    return redirect('doctor_dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
