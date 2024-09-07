from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(max_length=14, required=True)

    def save(self, request,*args, **kwargs):
        user = super(CustomSignupForm, self).save(request,*args, **kwargs)
        user.phone_number = self.cleaned_data['phone_number']
        user.save(*args, **kwargs)
        return user