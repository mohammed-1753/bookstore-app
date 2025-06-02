from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

# Login view
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            print("Form not valid")
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


# Logout view
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

# Home view (protected)
@login_required
def home(request):
    return render(request, 'main/home.html')
from .models import Note

@login_required
def dashboard(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'main/dashboard.html', {'notes': notes})

from .forms import NoteForm

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # ✅ link to logged-in user
            note.save()
            return redirect('dashboard')
    else:
        form = NoteForm()
    return render(request, 'main/create_note.html', {'form': form})
@login_required
def edit_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NoteForm(instance=note)
    return render(request, 'main/edit_note.html', {'form': form})
@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('dashboard')
    return render(request, 'main/delete_note.html', {'note': note})






