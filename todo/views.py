from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# READ + CREATE
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user   # 👈 assign owner
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'form': form
    })


# UPDATE
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/task_form.html', {'form': form})


# DELETE
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'todo/task_confirm_delete.html', {'task': task})

def home(request):
    if request.user.is_authenticated:
        return render(request, 'todo/home.html')
    return render(request, 'todo/home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # 👈 go to homepage, not logged in

    return render(request, 'todo/register.html', {'form': form})