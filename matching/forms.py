from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Application, Job, Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label="Jina la kwanza")
    last_name = forms.CharField(max_length=150, label="Jina la mwisho")
    email = forms.EmailField(label="Barua pepe")
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Ninajiunga kama")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role")
        labels = {"username": "Jina la mtumiaji"}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "phone",
            "location",
            "company_name",
            "skills",
            "education",
            "experience",
            "bio",
        ]
        labels = {
            "phone": "Namba ya simu",
            "location": "Eneo / mkoa",
            "company_name": "Jina la kampuni / taasisi",
            "skills": "Ujuzi (tenganisha kwa koma)",
            "education": "Elimu",
            "experience": "Uzoefu",
            "bio": "Kuhusu mimi / taasisi",
        }
        widgets = {
            "education": forms.Textarea(attrs={"rows": 3}),
            "experience": forms.Textarea(attrs={"rows": 3}),
            "bio": forms.Textarea(attrs={"rows": 3}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "company",
            "job_type",
            "location",
            "description",
            "requirements",
            "application_email",
            "deadline",
        ]
        labels = {
            "title": "Jina la nafasi",
            "company": "Kampuni / taasisi",
            "job_type": "Aina ya nafasi",
            "location": "Eneo",
            "description": "Maelezo ya nafasi",
            "requirements": "Ujuzi na vigezo",
            "application_email": "Barua pepe ya maombi (hiari)",
            "deadline": "Tarehe ya mwisho (hiari)",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "requirements": forms.Textarea(attrs={"rows": 3}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cover_letter"]
        labels = {"cover_letter": "Ujumbe / barua ya maombi (hiari)"}
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Eleza kwa kifupi kwa nini unafaa..."}
            )
        }
