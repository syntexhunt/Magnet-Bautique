from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Category, BlogModel

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'page']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'page': forms.Select(attrs={'class': 'form-control'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'content', 'image', 'category', 'page', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': FroalaEditor(),  # FroalaEditor widget
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'page': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image')
        if image_file:
            instance.save(image=image_file)
        if commit:
            instance.save()
        return instance
