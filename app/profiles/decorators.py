from django.shortcuts import get_object_or_404, redirect

from .models import Profile


def check_owner(view_func):
    def wrapper(request, slug, *args, **kwargs):
        existing = get_object_or_404(Profile, slug=slug)

        if existing.owner != request.user:
            return redirect('profile_view', slug=slug)
        else:
            return view_func(request, slug, *args, **kwargs)
    return wrapper
