from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Rating
from jobs.models import Job, JobApplication


@login_required
def rate_worker_view(request, job_pk, worker_pk):
    job = get_object_or_404(Job, pk=job_pk)
    worker = get_object_or_404(User, pk=worker_pk)

    if request.user != job.employer:
        messages.error(request, "Faqat ish beruvchi baholashi mumkin.")
        return redirect('home')

    if Rating.objects.filter(worker=worker, employer=request.user, job=job).exists():
        messages.warning(request, "Siz bu ishchini allaqachon baholagansiz.")
        return redirect('job_detail', pk=job.pk)

    # Check that worker was accepted for this job
    if not JobApplication.objects.filter(job=job, worker=worker, status='qabul_qilindi').exists():
        messages.error(request, "Bu ishchi sizning ishingizda qabul qilinmagan.")
        return redirect('job_detail', pk=job.pk)

    if request.method == 'POST':
        score = request.POST.get('score')
        comment = request.POST.get('comment', '')
        try:
            score = int(score)
            if 1 <= score <= 5:
                Rating.objects.create(
                    worker=worker,
                    employer=request.user,
                    job=job,
                    score=score,
                    comment=comment
                )
                messages.success(request, f"{worker.get_full_name() or worker.username} baholandi!")
                return redirect('job_detail', pk=job.pk)
        except (ValueError, TypeError):
            pass
        messages.error(request, "Noto'g'ri baho.")

    worker_profile = worker.profile
    return render(request, 'ratings/rate_worker.html', {
        'job': job,
        'worker': worker,
        'worker_profile': worker_profile,
        'range': range(1, 6),
    })


def worker_ratings_view(request, pk):
    worker = get_object_or_404(User, pk=pk)
    ratings = Rating.objects.filter(worker=worker).select_related('employer', 'job')
    avg = worker.profile.average_rating()
    return render(request, 'ratings/worker_ratings.html', {
        'worker': worker,
        'ratings': ratings,
        'avg': avg,
    })
