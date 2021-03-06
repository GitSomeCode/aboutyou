import operator

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView
from django.views.generic.edit import UpdateView

from .decorators import check_owner
from .forms import RegistrationForm, LoginForm, ProfileForm
from .models import Profile


def success(request):
    return HttpResponse('success!!!')


def register(request):
    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Creates the new user
            form.save()

            # Authenticate and log in user
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)

            if user and user.is_active:
                django_login(request, user)
                return redirect('all')
        else:
            print(form.errors)

    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated():
        return redirect('all')
    else:
        form = LoginForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                # Get user, log in user, redirect
                data = form.cleaned_data
                user = authenticate(email=data['email'], password=data['password'])
                django_login(request, user)
                return redirect('all')
            else:
                print(form.errors)

        return render(request, 'registration/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return redirect('login')


def index(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile_info = form.save(commit=False)
            profile_info.owner = request.user
            profile_info.save()
            form.save_m2m()
            return redirect('success')
        else:
            print form.errors
    else:
        form = ProfileForm()

    return render(request, 'profiles/fillout.html', {'form': form})


@login_required
@check_owner
def profile_update(request, slug, *args, **kwargs):
    '''
    Update a profile.
    '''

    existing = get_object_or_404(Profile, slug=slug)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=existing)

        if form.is_valid():
            profile_info = form.save(commit=False)
            profile_info.save()
            form.save_m2m()
            return redirect('all')
        else:
            print form.errors
    else:
        form = ProfileForm(instance=existing)

    return render(request, 'profiles/update_profile.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('all')


class ProfileView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profiles/profile_detail.html'


class ProfileList(View):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'profiles/all.html'

    def get(self, request, *args, **kwargs):
        query_list = request.GET.keys()
        if query_list:
            profiles = Profile.objects.filter(
                reduce(
                    operator.or_, (
                        Q(tags__name__contains=x) for x in query_list
                    )
                )
            ).distinct()
        else:
            profiles = Profile.objects.all()
        return render(request, 'profiles/all.html', {'profiles': profiles, 'search_tags': query_list})
