from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Profile
from .forms import ProfileForm

# Create your views here.
def success(request):
    return HttpResponse('success!!!')

def index(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            #import pdb; pdb.set_trace();
            profile_info = form.save(commit=False)
            profile_info.user = request.user
            profile_info.save()
            form.save_m2m()
            return redirect('success')
    else:
        form = ProfileForm()

    return render(request, 'profiles/fillout.html', {'form':form})

class ProfileView(ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'profiles/all.html'

