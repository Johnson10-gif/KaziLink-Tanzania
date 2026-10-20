from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .matching import match_score
from .models import Application, Job, Notification, Profile


class MatchingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="amina", password="test-password-123")
        self.profile = Profile.objects.create(
            user=self.user, role=Profile.SEEKER, skills="Python, SQL, Excel"
        )
        self.employer = User.objects.create_user(username="employer", password="test-password-123")
        Profile.objects.create(user=self.employer, role=Profile.EMPLOYER)
        self.job = Job.objects.create(
            employer=self.employer,
            title="Mchambuzi wa Data",
            company="Kampuni",
            job_type=Job.INTERNSHIP,
            location="Dar es Salaam",
            description="Nafasi ya mafunzo.",
            requirements="Python, SQL",
            deadline=date(2026, 12, 31),
        )

    def test_match_score_uses_overlapping_skills(self):
        self.assertEqual(match_score(self.profile, self.job), 100)

    def test_match_score_is_zero_when_profile_has_no_skills(self):
        self.profile.skills = ""
        self.assertEqual(match_score(self.profile, self.job), 0)

    def test_applicant_can_apply_and_employer_receives_notification(self):
        self.client.login(username="amina", password="test-password-123")
        response = self.client.post(reverse("job_detail", args=[self.job.id]), {"cover_letter": "Nina uzoefu."})
        self.assertRedirects(response, reverse("job_detail", args=[self.job.id]))
        self.assertEqual(Application.objects.filter(job=self.job, applicant=self.user).count(), 1)
        self.assertTrue(Notification.objects.filter(user=self.job.employer, job=self.job).exists())

    def test_employer_cannot_apply_to_a_job(self):
        self.client.login(username="employer", password="test-password-123")
        response = self.client.post(reverse("job_detail", args=[self.job.id]), {})
        self.assertRedirects(response, reverse("job_detail", args=[self.job.id]))
        self.assertFalse(Application.objects.filter(job=self.job).exists())

    def test_dashboard_recommendations_include_match_percentage(self):
        self.client.login(username="amina", password="test-password-123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100% match")

    def test_public_pages_render(self):
        for url in (
            reverse("home"),
            reverse("job_list"),
            reverse("job_detail", args=[self.job.id]),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_seeker_can_open_cv_builder(self):
        self.client.login(username="amina", password="test-password-123")
        response = self.client.get(reverse("cv_builder"))
        self.assertEqual(response.status_code, 200)

    def test_employer_dashboard_and_job_form_render(self):
        self.client.login(username="employer", password="test-password-123")
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)
        self.assertEqual(self.client.get(reverse("create_job")).status_code, 200)

    def test_signup_creates_user_profile_and_authenticates(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "neema",
                "first_name": "Neema",
                "last_name": "Mushi",
                "email": "neema@example.com",
                "role": Profile.SEEKER,
                "password1": "Strong!Test-2026-xx",
                "password2": "Strong!Test-2026-xx",
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="neema")
        self.assertEqual(user.profile.role, Profile.SEEKER)
