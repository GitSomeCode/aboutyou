import operator

from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView
from django.views.generic.edit import UpdateView

from .decorators import check_owner
from .forms import ProfileForm, RegistrationForm
from .models import Profile


def success(request):
    return HttpResponse('success!!!')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user.set_password(new_user.password)
            new_user.save()

            # Authenticate user and log in.
            username = new_user.username
            password = new_user.password
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('custom_login')
        else:
            print form.errors
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    if request.user.is_authenticated():
        return redirect('all')
    else:
        return login(request)


def custom_logout(request):
    logout(request)
    return redirect('custom_login')


def index(request):
    print request.META.get('REMOTE_ADDR', None)
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
