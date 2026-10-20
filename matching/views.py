from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ApplicationForm, JobForm, ProfileForm, SignUpForm
from .matching import match_score, matching_jobs
from .models import Application, Job, Notification, Profile


def _profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def home(request):
    jobs = Job.objects.filter(is_active=True)
    featured = list(jobs[:6])
    if request.user.is_authenticated:
        profile = _profile(request.user)
        if profile.role == Profile.SEEKER:
            featured = matching_jobs(profile, featured)
    return render(
        request,
        "matching/home.html",
        {
            "jobs": featured,
            "job_count": jobs.count(),
            "employer_count": Profile.objects.filter(role=Profile.EMPLOYER).count(),
            "seeker_count": Profile.objects.filter(role=Profile.SEEKER).count(),
        },
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=form.cleaned_data["role"])
            login(request, user)
            messages.success(request, "Akaunti yako imetengenezwa. Karibu!")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    query = request.GET.get("q", "").strip()
    job_type = request.GET.get("type", "").strip()
    location = request.GET.get("location", "").strip()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query)
            | Q(company__icontains=query)
            | Q(description__icontains=query)
            | Q(requirements__icontains=query)
        )
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)

    jobs = list(jobs)
    if request.user.is_authenticated:
        profile = _profile(request.user)
        if profile.role == Profile.SEEKER:
            jobs = matching_jobs(profile, jobs)
    return render(
        request,
        "matching/job_list.html",
        {"jobs": jobs, "query": query, "selected_type": job_type, "location": location},
    )


def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    profile = _profile(request.user) if request.user.is_authenticated else None
    application = None
    if profile and profile.role == Profile.SEEKER:
        application = Application.objects.filter(job=job, applicant=request.user).first()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        if job.employer_id == request.user.id or not profile or profile.role != Profile.SEEKER:
            messages.error(request, "Maombi yanapatikana kwa akaunti za watafuta kazi pekee.")
            return redirect("job_detail", job_id=job.id)
        if not job.is_active:
            messages.error(request, "Nafasi hii haipokei maombi kwa sasa.")
            return redirect("job_detail", job_id=job.id)
        if application:
            messages.info(request, "Umeshawasilisha maombi ya nafasi hii.")
            return redirect("job_detail", job_id=job.id)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            Notification.objects.create(
                user=job.employer,
                message=f"Maombi mapya ya {job.title} kutoka {request.user.get_full_name() or request.user.username}.",
                job=job,
            )
            messages.success(request, "Maombi yako yametumwa kwa mwajiri.")
            return redirect("job_detail", job_id=job.id)
    else:
        form = ApplicationForm()
    return render(
        request,
        "matching/job_detail.html",
        {
            "job": job,
            "form": form,
            "application": application,
            "match_percent": match_score(profile, job) if profile and profile.role == Profile.SEEKER else None,
        },
    )


@login_required
def dashboard(request):
    profile = _profile(request.user)
    notifications = Notification.objects.filter(user=request.user)[:5]
    if profile.role == Profile.EMPLOYER:
        jobs = Job.objects.filter(employer=request.user)
        applications = Application.objects.filter(job__employer=request.user).select_related(
            "job", "applicant"
        )
        context = {
            "profile": profile,
            "jobs": jobs,
            "applications": applications[:8],
            "application_count": applications.count(),
            "notifications": notifications,
        }
        return render(request, "matching/dashboard_employer.html", context)

    applications = Application.objects.filter(applicant=request.user).select_related("job")
    recommendations = matching_jobs(
        profile, list(Job.objects.filter(is_active=True).exclude(applications__applicant=request.user))
    )[:4]
    return render(
        request,
        "matching/dashboard_seeker.html",
        {
            "profile": profile,
            "applications": applications[:5],
            "application_count": applications.count(),
            "recommendations": recommendations,
            "notifications": notifications,
        },
    )


@login_required
def profile_edit(request):
    profile = _profile(request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Taarifa zako zimehifadhiwa.")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "matching/profile_form.html", {"form": form, "profile": profile})


@login_required
def cv_builder(request):
    profile = _profile(request.user)
    if profile.role != Profile.SEEKER:
        messages.error(request, "CV builder inapatikana kwa watafuta kazi pekee.")
        return redirect("dashboard")
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Taarifa za CV zimehifadhiwa.")
            return redirect("cv_builder")
    else:
        form = ProfileForm(instance=profile)
    return render(
        request,
        "matching/cv_builder.html",
        {"form": form, "profile": profile, "print_view": request.GET.get("print") == "1"},
    )


@login_required
def create_job(request):
    profile = _profile(request.user)
    if profile.role != Profile.EMPLOYER:
        messages.error(request, "Ni waajiri pekee wanaoweza kuchapisha nafasi.")
        return redirect("dashboard")
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            if not job.company:
                job.company = profile.company_name or request.user.get_full_name()
            job.save()
            matching_profiles = [
                candidate
                for candidate in Profile.objects.filter(role=Profile.SEEKER).select_related("user")
                if match_score(candidate, job) > 0
            ]
            Notification.objects.bulk_create(
                [
                    Notification(
                        user=candidate.user,
                        job=job,
                        message=f"Nafasi mpya ya {job.title} inalingana na ujuzi wako.",
                    )
                    for candidate in matching_profiles
                ]
            )
            messages.success(request, "Nafasi imechapishwa na watafuta kazi wanaolingana wamearifiwa.")
            return redirect("dashboard")
    else:
        form = JobForm(initial={"company": profile.company_name})
    return render(request, "matching/job_form.html", {"form": form})


@login_required
@require_POST
def update_application_status(request, application_id):
    application = get_object_or_404(
        Application.objects.select_related("job"), pk=application_id, job__employer=request.user
    )
    status = request.POST.get("status")
    valid_statuses = {choice[0] for choice in Application.STATUS_CHOICES}
    if status not in valid_statuses:
        messages.error(request, "Hali uliyochagua si sahihi.")
    else:
        application.status = status
        application.save(update_fields=["status"])
        Notification.objects.create(
            user=application.applicant,
            job=application.job,
            message=f"Hali ya maombi yako ya {application.job.title} imebadilika: {application.get_status_display()}.",
        )
        messages.success(request, "Hali ya maombi imesasishwa.")
    return redirect("dashboard")


@login_required
@require_POST
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect("dashboard")
