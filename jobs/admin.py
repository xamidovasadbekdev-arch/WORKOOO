from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'category', 'region', 'salary', 'status', 'created_at']
    list_filter = ['status', 'region', 'category']
    search_fields = ['title', 'description', 'employer__username']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'worker', 'status', 'created_at']
    list_filter = ['status']
