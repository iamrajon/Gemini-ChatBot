
from django import forms

# form for uploading text and image for request to gemini api
class TextAndImageForm(forms.Form):
    
    image_field = forms.ImageField(
        label="Choose Image",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    text_field = forms.CharField(
        max_length=100,
        label="Describe Image",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
