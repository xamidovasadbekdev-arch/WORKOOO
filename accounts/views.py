from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, ProfileEditForm
from .models import UserProfile
from ratings.models import Rating


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Role comes from hidden input (tab selector), not form field
            role = request.POST.get('role', 'worker')
            if role not in ('worker', 'employer'):
                role = 'worker'
            # Override the role in cleaned_data so forms.py save() uses correct role
            form.cleaned_data['role'] = role
            user = form.save(commit=True)  # forms.py save() creates UserProfile
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}! Hisobingiz muvaffaqiyatli yaratildi.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            error = "Foydalanuvchi nomi yoki parol noto'g'ri."
    return render(request, 'accounts/login.html', {'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_own_view(request):
    """O'z profili - login talab qilinadi"""
    profile_user = request.user
    # Auto-create profile if missing (old accounts without UserProfile)
    profile, _ = UserProfile.objects.get_or_create(
        user=profile_user,
        defaults={'role': 'worker'}
    )
    ratings = Rating.objects.filter(worker=profile_user).select_related('employer', 'job')
    avg = profile.average_rating()
    posted_jobs = profile_user.posted_jobs.all()[:5] if profile.role == 'employer' else None
    applied_jobs = profile_user.applications.select_related('job').all()[:5] if profile.role == 'worker' else None

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'ratings': ratings,
        'avg': avg,
        'posted_jobs': posted_jobs,
        'applied_jobs': applied_jobs,
        'is_own': True,
    })


def profile_view(request, pk):
    """Boshqa foydalanuvchi profili - ommaviy"""
    profile_user = get_object_or_404(User, pk=pk)
    # Auto-create profile if missing
    profile, _ = UserProfile.objects.get_or_create(
        user=profile_user,
        defaults={'role': 'worker'}
    )
    ratings = Rating.objects.filter(worker=profile_user).select_related('employer', 'job')
    avg = profile.average_rating()
    posted_jobs = profile_user.posted_jobs.all()[:5] if profile.role == 'employer' else None
    applied_jobs = profile_user.applications.select_related('job').all()[:5] if profile.role == 'worker' else None

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'ratings': ratings,
        'avg': avg,
        'posted_jobs': posted_jobs,
        'applied_jobs': applied_jobs,
        'is_own': request.user.is_authenticated and request.user == profile_user,
    })


@login_required
def profile_edit_view(request):
    # Use get_or_create to avoid 404 for old accounts without UserProfile
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'worker'}
    )
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            updated_profile = form.save(commit=False)
            # Save role change if provided
            new_role = request.POST.get('role')
            if new_role in ('worker', 'employer'):
                updated_profile.role = new_role
            updated_profile.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('profile_own')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form, 'profile': profile})
