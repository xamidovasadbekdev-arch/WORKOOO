from django.db import models
from django.contrib.auth.models import User
from accounts.models import REGIONS

JOB_CATEGORIES = [
    ('qurilish', 'Qurilish va ta\'mirlash'),
    ('yuk_tashish', 'Yuk tashish va ko\'chirish'),
    ('tozalash', 'Tozalash xizmati'),
    ('qishloq', 'Qishloq xo\'jaligi'),
    ('savdo', 'Savdo va xizmat'),
    ('it', 'IT va kompyuter'),
    ('ta\'lim', 'Ta\'lim va repetitorlik'),
    ('sog\'liqni_saqlash', 'Sog\'liqni saqlash'),
    ('cafe', 'Cafe va restoran'),
    ('boshqa', 'Boshqa'),
]

JOB_STATUS = [
    ('ochiq', 'Ochiq'),
    ('yopiq', 'Yopiq'),
    ('tugallangan', 'Tugallangan'),
]

APPLICATION_STATUS = [
    ('kutilmoqda', 'Kutilmoqda'),
    ('qabul_qilindi', 'Qabul qilindi'),
    ('rad_etildi', 'Rad etildi'),
]


class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=JOB_CATEGORIES, default='boshqa')
    salary = models.DecimalField(max_digits=12, decimal_places=0, help_text="So'mda")
    salary_type = models.CharField(max_length=20, choices=[('kunlik', 'Kunlik'), ('soatlik', 'Soatlik'), ('loyiha', 'Loyiha')], default='kunlik')
    region = models.CharField(max_length=50, choices=REGIONS, default='toshkent_shahar')
    address = models.CharField(max_length=300)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='job_images/', blank=True, null=True)
    workers_needed = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='ochiq')
    work_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def application_count(self):
        return self.applications.count()

    def accepted_count(self):
        return self.applications.filter(status='qabul_qilindi').count()

    def get_salary_display_text(self):
        salary = f"{int(self.salary):,}".replace(',', ' ')
        return f"{salary} so'm / {self.get_salary_type_display()}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='kutilmoqda')
    message = models.TextField(blank=True, max_length=500, help_text="Qo'shimcha xabar (ixtiyoriy)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'worker')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.worker.username} → {self.job.title} ({self.get_status_display()})"
