from typing import Any
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self) -> dict[str, Any]:
        data = dict(self.cleaned_data)
        title = data.get('title')
        qs = Article.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', f"{title} already in used")
        return super().clean()
