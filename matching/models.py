from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    SEEKER = "seeker"
    EMPLOYER = "employer"
    ROLE_CHOICES = [(SEEKER, "Mtafuta kazi"), (EMPLOYER, "Mwajiri")]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default=SEEKER)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=160, blank=True)
    skills = models.TextField(blank=True, help_text="Tenganisha ujuzi kwa koma.")
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def skill_list(self):
        return [skill.strip() for skill in self.skills.split(",") if skill.strip()]


class Job(models.Model):
    FULL_TIME = "full_time"
    INTERNSHIP = "internship"
    VOLUNTEER = "volunteer"
    GIG = "gig"
    JOB_TYPES = [
        (FULL_TIME, "Ajira"),
        (INTERNSHIP, "Internship"),
        (VOLUNTEER, "Kujitolea"),
        (GIG, "Kujishikiza"),
    ]

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs"
    )
    title = models.CharField(max_length=180)
    company = models.CharField(max_length=160)
    job_type = models.CharField(max_length=16, choices=JOB_TYPES)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(help_text="Orodhesha ujuzi au vigezo, kwa koma au mistari.")
    application_email = models.EmailField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.company}"


class Application(models.Model):
    PENDING = "pending"
    REVIEWING = "reviewing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    STATUS_CHOICES = [
        (PENDING, "Imepokelewa"),
        (REVIEWING, "Inapitiwa"),
        (ACCEPTED, "Amechaguliwa"),
        (REJECTED, "Hajachaguliwa"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["job", "applicant"], name="unique_application_per_applicant_job"
            )
        ]

    def __str__(self):
        return f"{self.applicant} → {self.job}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=240)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message
