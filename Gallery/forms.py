from django import forms
from .models import Picture


class ImageUploadForm(forms.Form):
    title = forms.CharField(max_length=200)
    image = forms.ImageField()
    content = forms.CharField(widget=forms.Textarea)


class ImageUpdateForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['title', 'content', 'image']