from typing import Any
from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
    """
    Validation or clean methods, to validate forms or validate the forms we have two methods
    1. field specific validation
    2. whole form validation
    """

    # field validation, to do field validation create a method called clean_<your field name>(self)

    # def clean_title(self) -> str:
    #     # Dictionary containing the field i.e it will only be containing title only ({'title': 'value'})
    #     cleaned_data = dict(self.cleaned_data)
    #     title = cleaned_data.get('title')
    #     # add validation logic here
    #     if 'form' in title.lower():
    #         raise forms.ValidationError(
    #             'substring form can not be present in title')

    #     return title

    # whole form validation declare method called clean(self)
    # remember you can not have field validation methods if you have whole form validation method.

    def clean(self) -> dict[str, Any]:
        form_str = 'form'
        # Dictionary containing all of the fields ({'title': 'value','content':'value'})
        cleaned_data = dict(self.cleaned_data)
        title = str(cleaned_data.get('title'))
        content = str(cleaned_data.get('content'))
        # here can also throw both type of error field error as well as non-field error
        if form_str in content.lower() and form_str in title.lower():
            raise forms.ValidationError(
                'substring form present in both, content and title')
        
        if form_str in title.lower():
            self.add_error(field='title',error='title contains substring form')

        if form_str in content.lower():
            self.add_error(field='content',error='content contains substring form')

        return cleaned_data
