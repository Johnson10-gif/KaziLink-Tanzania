import re


def _normalize(value):
    return {
        token.lower()
        for token in re.findall(r"[a-zA-Z0-9+#.]+", value or "")
        if len(token) > 1
    }


def match_score(profile, job):
    """Return a percentage based on overlap between applicant skills and job criteria."""
    skills = _normalize(profile.skills)
    requirements = _normalize(job.requirements)
    if not skills or not requirements:
        return 0
    return round(len(skills & requirements) / len(requirements) * 100)


def matching_jobs(profile, jobs):
    for job in jobs:
        job.match_percent = match_score(profile, job)
    return sorted(jobs, key=lambda job: (job.match_percent, job.created_at), reverse=True)
