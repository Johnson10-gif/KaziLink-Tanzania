from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("akaunti/jisajili/", views.signup, name="signup"),
    path("nafasi/", views.job_list, name="job_list"),
    path("nafasi/<int:job_id>/", views.job_detail, name="job_detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("wasifu/", views.profile_edit, name="profile_edit"),
    path("cv/", views.cv_builder, name="cv_builder"),
    path("waajiri/nafasi-mpya/", views.create_job, name="create_job"),
    path(
        "maombi/<int:application_id>/hali/",
        views.update_application_status,
        name="update_application_status",
    ),
    path("arifa/soma/", views.mark_notifications_read, name="mark_notifications_read"),
]
