from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Product, Version, BlogPost


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'manufactured_at']


    def clean_name(self):
        banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        name = self.cleaned_data.get('name')
        for word in banned_words:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"The word '{word}' is not allowed in the product name.")
        return name

    def clean_description(self):
        banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        description = self.cleaned_data.get('description')
        for word in banned_words:
            if word.lower() in description.lower():
                raise forms.ValidationError(f"The word '{word}' is not allowed in the product description.")
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current']

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_current'].widget.attrs['class'] = 'form-check-input'


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'published']



