from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Sezione , Discussione , Post

class RegistrazioneUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'inserisci password'}))
    conferma_password = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'conferma password'}))

    class Meta:
        model = User
        fields = ['username','email','password','conferma_password']


    def clean(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['conferma_password']
        if pass1 != pass2:
            raise ValidationError('Le password non coincidono , per favore , riprova')
        return self.cleaned_data


class CreaSezioneForm(forms.ModelForm):

    class Meta:
        model = Sezione
        fields = "__all__"


class CreaDiscussioneForm(forms.ModelForm):

    class Meta:
        model = Discussione
        fields = ['titolo','primo_post',]



class CreaPostForm(forms.ModelForm):

    contenuto = forms.CharField(widget=forms.Textarea(attrs={
        'rows':10
    }))

    class Meta:
        model = Post
        fields = ['contenuto']
        labels = {'contenuto':'Rispondi'}