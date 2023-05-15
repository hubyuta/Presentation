from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label='Search', max_length=100)

class ContactForm(forms.Form):
    name = forms.CharField(required=True,max_length=30)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=30)
    message = forms.CharField(required=True, min_length=10, max_length=500,widget=forms.Textarea)

    def send_email(self):
        pass
