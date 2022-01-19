import re
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #allows to craete form and pass forward to template
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET': #comes from signupuser.html being accessed
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        #create new user if form on signup.html makes a post by clicking button
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1']) #function pulled from django where 'username' and 'password1' can be viewed by inspecting page an hovering what was made by User CreationForm
                user.save() #saves new user into database
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': 'That username has already been taken, please choose a new one'})
        else:
            #tell user passwords didnt match
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET': #comes from loginuser.html being accessed
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method  == 'POST': #must be a post request bc many browser will automatically load a tag get requests and that would log user out
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
        todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
        return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST) #take info user put in TodoForm
            newtodo = form.save(commit=False)
            newtodo.user = request.user #specifies user
            newtodo.save() #puts info in database
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error': 'Bad data passed in. Try again'})

@login_required
def viewtodo(request, todo_pk):
        todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #grabs todo object if it matches user and pk
        if request.method == 'GET':
            form = TodoForm(instance=todo)
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
        else:
            try:
                form = TodoForm(request.POST, instance=todo)
                form.save()
                return redirect('currenttodos')
            except ValueError:
                return render(request, 'todo/createtodo.html', {'todo':todo, 'error': 'Bad data passed in. Try again'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
 
@login_required
def completedtodos(request):
        todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
        return render(request, 'todo/completedtodos.html', {'todos':todos})