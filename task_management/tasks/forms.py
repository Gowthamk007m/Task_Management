from django import forms
from django.contrib.auth.models import User
from .models import Task, UserProfile


class TaskForm(forms.ModelForm):
    """Full task form for admins"""
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 
                  'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'completion_report': forms.Textarea(attrs={'rows': 4}),
        }


class TaskUpdateForm(forms.ModelForm):
    """Limited task form for regular users"""
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
        widgets = {
            'completion_report': forms.Textarea(attrs={'rows': 4}),
        }
        

class UserProfileForm(forms.ModelForm):
    """Form for updating user profiles"""
    class Meta:
        model = UserProfile
        fields = ['role']