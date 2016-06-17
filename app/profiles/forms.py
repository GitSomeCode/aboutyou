from django import forms
from django.contrib.auth import authenticate

from .models import Profile, User


class RegistrationForm(forms.ModelForm):
    '''
    Form for registering a new user.
    '''
    email = forms.EmailField(widget=forms.widgets.TextInput, label='Email')
    password1 = forms.CharField(widget=forms.widgets.PasswordInput, label='password')
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, label='password confirmation')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_password(self):
        '''
        Check that both passwords match.
        '''
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        '''
        Save provided password in hashed format.
        '''
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    '''
    Login and authenticate user.
    '''
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        is_user = authenticate(email=email, password=password)

        if not is_user:
            raise forms.ValidationError("Invalid email or password. Please try again.")

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    '''
    Profile creation/update form.
    '''
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'location', 'spotlight', 'image', 'tags']

    def clean_tags(self):
        """
        Allow only 5 tags, and convert to lowercase.
        """
        tags = self.cleaned_data.get('tags', None)

        if len(tags) < 3:
            raise forms.ValidationError("Atleast 3 tags.")
        elif len(tags) > 5:
            raise forms.ValidationError("At most 5 tags.")

        tags = [tag.lower() for tag in tags]

        return tags