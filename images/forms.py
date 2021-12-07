from django import forms
from django.core.files.base import ContentFile
from .models import Image
from django.utils.text import slugify
from urllib import request

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('the given url does not contains valid image extensions')
        return url

    def save(self, commit=True, force_insert=False, force_update=False):
        image = super().save(commit=False)
        url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        response = request.urlopen(url)
        image.image.save(image_name, ContentFile(response.read()),
                         save=False)

        if commit:
            image.save()
        return  image

