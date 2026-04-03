from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, REGIONS, ROLES


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Ismi")
    last_name = forms.CharField(max_length=50, required=True, label="Familiyasi")
    email = forms.EmailField(required=False, label="Email (ixtiyoriy)")
    role = forms.ChoiceField(choices=ROLES, label="Siz kim sifatida kirasiz?", required=False, initial='worker')
    region = forms.ChoiceField(choices=[('', '-- Viloyatni tanlang --')] + list(REGIONS), label="Viloyat")
    phone = forms.CharField(max_length=20, required=False, label="Telefon raqam (ixtiyoriy)")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Foydalanuvchi nomi',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Bu foydalanuvchi nomi allaqachon band. Boshqa nom tanlang."
            )
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data.get('role') or 'worker',
                region=self.cleaned_data.get('region', ''),
                phone=self.cleaned_data.get('phone', ''),
            )
        return user


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Ismi")
    last_name = forms.CharField(max_length=50, required=True, label="Familiyasi")
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = UserProfile
        fields = ['avatar', 'region', 'bio', 'phone']
        labels = {
            'avatar': 'Profil rasmi',
            'region': 'Viloyat',
            'bio': 'O\'zingiz haqingizda',
            'phone': 'Telefon raqam',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
