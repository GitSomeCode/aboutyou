from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from .models import Profile
from .forms import ProfileForm

# Create your views here.
'''
def owns_profile(user):
    return user.profile.owner == request.profile.owner
'''

def success(request):
    raise Http404

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

    return render(request, 'profiles/fillout.html', {'form':form})

def check_owner(view_func):
    def wrapper(request, slug, *args, **kwargs):
        existing = get_object_or_404(Profile, slug=slug)

        if existing.owner != request.user:
            return redirect('profile_view', slug=slug)
        else:
            return view_func(request, slug, *args, **kwargs)
    return wrapper

@login_required
@check_owner
def profile_update(request, slug, *args, **kwargs):
    
    existing = get_object_or_404(Profile, slug=slug)

    '''
    if existing.owner != request.user:
        #import pdb; pdb.set_trace();
        #slug = request.user.profile.slug
        return redirect('profile_view', slug=slug)
    else:
    '''
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

    return render(request, 'profiles/update_profile.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    #fields = ['first_name', 'last_name', 'location', 'spotlight', 'image', 'tags']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('all')


class ProfileView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profiles/profile_detail.html'

class ProfileList(ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'profiles/all.html'

