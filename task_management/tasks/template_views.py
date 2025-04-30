from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import Task, UserProfile
from .forms import TaskForm, TaskUpdateForm
from .permissions import is_admin, is_super_admin
from django.utils import timezone


# Dashboard/Home view
@login_required

def home(request):
    user = request.user
    is_admin_user = is_admin(user)
    is_super_user = is_super_admin(user)

    if is_admin_user or is_super_user:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=user)

    tasks = tasks.select_related('assigned_to')  # for optimization

    context = {
        'user': user,
        'is_admin': is_admin_user,
        'is_super_admin': is_super_user,
        'tasks': tasks,
        'next_due_task': tasks.order_by('due_date').first(),
        'recent_tasks': tasks.order_by('-created_at')[:5],
        'due_soon_tasks': tasks.order_by('due_date')[:5],
        'now': timezone.now(),
    }

    return render(request, 'tasks/dashboard.html', context)


# User management views (for SuperAdmin)
@login_required
def user_list(request):
    """List all users (SuperAdmin only)"""
    if not is_super_admin(request.user):
        messages.error(request, "You don't have permission to view this page.")
        return redirect('home')
    
    users = User.objects.all()
    return render(request, 'tasks/user_list.html', {'users': users})


@login_required
def user_detail(request, pk):
    """View user details (SuperAdmin only)"""
    if not is_super_admin(request.user):
        messages.error(request, "You don't have permission to view this page.")
        return redirect('home')
    
    user = get_object_or_404(User, pk=pk)
    return render(request, 'tasks/user_detail.html', {'user': user})


# Task management views
@login_required
def task_list(request):
    """View all tasks based on user role"""
    user = request.user
    
    if is_admin(user) or is_super_admin(user):
        # Admins see all tasks
        tasks = Task.objects.all()
    else:
        # Regular users see only their tasks
        tasks = Task.objects.filter(assigned_to=user)
    
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, pk):
    """View task details"""
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    
    # Check if user has permission to view this task
    if not (is_admin(user) or is_super_admin(user) or task.assigned_to == user):
        messages.error(request, "You don't have permission to view this task.")
        return redirect('task_list')
    
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    """Create a new task (Admin only)"""
    if not (is_admin(request.user) or is_super_admin(request.user)):
        messages.error(request, "You don't have permission to create tasks.")
        return redirect('task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created successfully.")
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_update(request, pk):
    """Update a task"""
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    
    # Check permissions
    if not (is_admin(user) or is_super_admin(user) or task.assigned_to == user):
        messages.error(request, "You don't have permission to update this task.")
        return redirect('task_list')
    
    # Use different form based on user role
    if is_admin(user) or is_super_admin(user):
        form_class = TaskForm
    else:
        form_class = TaskUpdateForm  # Limited form for regular users
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=task)
        if form.is_valid():
            # For regular users completing a task, validate completion report and worked hours
            if not (is_admin(user) or is_super_admin(user)) and form.cleaned_data.get('status') == 'COMPLETED':
                if not form.cleaned_data.get('completion_report'):
                    form.add_error('completion_report', "Completion report is required when marking a task as completed.")
                if not form.cleaned_data.get('worked_hours'):
                    form.add_error('worked_hours', "Worked hours must be provided when marking a task as completed.")
                
                if form.errors:
                    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update', 'task': task})
            
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully.")
            return redirect('task_detail', pk=task.pk)
    else:
        form = form_class(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update', 'task': task})


@login_required
def task_report(request, pk):
    """View task report (Admin only, completed tasks only)"""
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    
    # Check permissions
    if not (is_admin(user) or is_super_admin(user)):
        messages.error(request, "You don't have permission to view task reports.")
        return redirect('task_list')
    
    # Check if task is completed
    if task.status != 'COMPLETED':
        messages.error(request, "Report is only available for completed tasks.")
        return redirect('task_detail', pk=task.pk)
    
    return render(request, 'tasks/task_report.html', {'task': task})