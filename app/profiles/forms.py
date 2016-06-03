from django import forms
from django.forms import ModelForm
from profiles.models import Profile


class ProfileForm(ModelForm):

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
