from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['worker', 'employer', 'job', 'score', 'created_at']
    list_filter = ['score']
