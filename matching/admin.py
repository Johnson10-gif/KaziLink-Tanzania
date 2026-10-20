from django.contrib import admin

from .models import Application, Job, Notification, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "location", "company_name")
    list_filter = ("role", "location")
    search_fields = ("user__username", "user__email", "company_name", "skills")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "job_type", "location", "is_active", "created_at")
    list_filter = ("job_type", "is_active", "location")
    search_fields = ("title", "company", "description", "requirements")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "applicant", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("job__title", "applicant__username")


admin.site.register(Notification)
