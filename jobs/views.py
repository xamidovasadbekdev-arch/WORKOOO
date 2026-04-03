from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm
from accounts.models import REGIONS, UserProfile


def home_view(request):
    jobs = Job.objects.filter(status='ochiq').select_related('employer', 'employer__profile')[:8]
    return render(request, 'home.html', {'jobs': jobs, 'regions': REGIONS})


def job_list_view(request):
    jobs = Job.objects.filter(status='ochiq').select_related('employer', 'employer__profile')
    region = request.GET.get('region', '')
    category = request.GET.get('category', '')
    q = request.GET.get('q', '')

    if region:
        jobs = jobs.filter(region=region)
    if category:
        jobs = jobs.filter(category=category)
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q))

    from .models import JOB_CATEGORIES
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'regions': REGIONS,
        'categories': JOB_CATEGORIES,
        'selected_region': region,
        'selected_category': category,
        'q': q,
    })


def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    user_application = None
    has_conversation = False

    if request.user.is_authenticated:
        try:
            user_application = JobApplication.objects.get(job=job, worker=request.user)
        except JobApplication.DoesNotExist:
            pass

        from chat.models import Conversation
        has_conversation = Conversation.objects.filter(
            job=job, worker=request.user
        ).exists() or Conversation.objects.filter(
            job=job, employer=request.user
        ).exists()

    form = JobApplicationForm()
    applications = None
    if request.user == job.employer:
        applications = job.applications.select_related('worker', 'worker__profile').all()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'user_application': user_application,
        'form': form,
        'applications': applications,
        'has_conversation': has_conversation,
    })


@login_required
def job_create_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.role != 'employer':
        messages.error(request, "Faqat ish beruvchilar ish e'lon qila oladi.")
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "Ish e'loni muvaffaqiyatli joylashtirildi!")
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_create.html', {'form': form})


@login_required
def job_edit_view(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Ish e'loni yangilandi!")
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_create.html', {'form': form, 'edit': True, 'job': job})


@login_required
def job_delete_view(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Ish e'loni o'chirildi.")
        return redirect('my_jobs')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def my_jobs_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.role != 'employer':
        return redirect('my_applications')
    jobs = Job.objects.filter(employer=request.user).prefetch_related('applications')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@login_required
def my_applications_view(request):
    applications = JobApplication.objects.filter(worker=request.user).select_related('job', 'job__employer', 'job__employer__profile')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def apply_job_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != 'worker':
        messages.error(request, "Faqat ishchilar ariza topshira oladi.")
        return redirect('job_detail', pk=pk)

    if request.user == job.employer:
        messages.error(request, "O'z e'loningizga ariza topshira olmaysiz.")
        return redirect('job_detail', pk=pk)

    if JobApplication.objects.filter(job=job, worker=request.user).exists():
        messages.warning(request, "Siz allaqachon bu ishga ariza topshirgansiz.")
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.worker = request.user
            app.save()
            messages.success(request, "Arizangiz yuborildi! Ish beruvchi tasdiqlashini kuting.")
            return redirect('job_detail', pk=pk)
    return redirect('job_detail', pk=pk)


@login_required
def manage_application_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.user != application.job.employer:
        messages.error(request, "Ruxsat yo'q.")
        return redirect('home')

    action = request.POST.get('action')
    if action == 'accept':
        application.status = 'qabul_qilindi'
        application.save()

        # Create conversation
        from chat.models import Conversation
        conversation, created = Conversation.objects.get_or_create(
            job=application.job,
            employer=request.user,
            worker=application.worker
        )
        messages.success(request, f"{application.worker.get_full_name() or application.worker.username} qabul qilindi. Chat ochildi!")
        return redirect('conversation_detail', pk=conversation.pk)

    elif action == 'reject':
        application.status = 'rad_etildi'
        application.save()
        messages.info(request, "Ariza rad etildi.")

    return redirect('job_detail', pk=application.job.pk)


@login_required
def complete_job_view(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        job.status = 'tugallangan'
        job.save()
        messages.success(request, "Ish tugallangan deb belgilandi.")
    return redirect('my_jobs')
