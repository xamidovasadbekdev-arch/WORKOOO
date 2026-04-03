from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='conversations')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer_conversations')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'employer', 'worker')
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat: {self.worker.username} ↔ {self.employer.username} ({self.job.title})"

    def last_message(self):
        return self.messages.order_by('-timestamp').first()

    def unread_count(self, user):
        return self.messages.exclude(sender=user).filter(is_read=False).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.body[:50]}"
