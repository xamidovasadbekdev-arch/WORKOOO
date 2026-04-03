from django.db import models
from django.contrib.auth.models import User

REGIONS = [
    ('toshkent_shahar', "Toshkent shahri"),
    ('toshkent_viloyat', "Toshkent viloyati"),
    ('andijon', "Andijon viloyati"),
    ('fargona', "Farg'ona viloyati"),
    ('namangan', "Namangan viloyati"),
    ('samarqand', "Samarqand viloyati"),
    ('buxoro', "Buxoro viloyati"),
    ('qashqadaryo', "Qashqadaryo viloyati"),
    ('surxondaryo', "Surxondaryo viloyati"),
    ('jizzax', "Jizzax viloyati"),
    ('sirdaryo', "Sirdaryo viloyati"),
    ('navoiy', "Navoiy viloyati"),
    ('xorazm', "Xorazm viloyati"),
    ('qoraqalpogiston', "Qoraqalpog'iston Respublikasi"),
]

ROLES = [
    ('worker', 'Ishchi'),
    ('employer', 'Ish beruvchi'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLES, default='worker')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGIONS, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/img/default_avatar.svg'

    def average_rating(self):
        from ratings.models import Rating
        ratings = Rating.objects.filter(worker=self.user)
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return None

    def rating_count(self):
        from ratings.models import Rating
        return Rating.objects.filter(worker=self.user).count()

    def get_region_display_name(self):
        for key, val in REGIONS:
            if key == self.region:
                return val
        return ''
