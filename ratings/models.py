from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 dan 5 gacha baho"
    )
    comment = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('worker', 'employer', 'job')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employer.username} → {self.worker.username}: {self.score}⭐"
