from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EmailForm(forms.Form):
    email = forms.EmailField(required=True, max_length=100, widget=forms.EmailInput(attrs={'placeholder':"Enter your email"}))


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password and comfirm password not match!")
        else:
            return cleaned_data


class EditProfileForm(forms.Form):
    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    file = forms.ImageField(required=False)
    name = forms.CharField(max_length=255,  widget=forms.TextInput(attrs={'value':""}))
    gender = forms.CharField(widget=forms.Select(choices=CHOICES))
    date = forms.CharField(255)
    username = forms.CharField(255)

    email = forms.CharField(max_length=255)


class UpdateNewAccountForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password and comfirm password not match!")
        else:
            return cleaned_data

class UpdateSkillsForm(forms.Form):
    date_start = forms.DateField(widget = forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))
    date_end = forms.DateField(widget = forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))

class AddSkillForm(forms.Form):
    skills = session.query(Skill).all()
    CHOICE =()
    for s in skills:
        tuple = (s.name, s.name)
        CHOICE   =  CHOICE + (tuple,)
        # print(CHOICE)
    skills = forms.CharField(widget=forms.Select(choices=CHOICE),)
    date_start = forms.DateField(widget = forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))
    date_end = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))

class RelationshipForm(forms.Form):
    CHOICES = (('wife', 'Wife'), ('son', 'Son'), ('father', 'Father'), ('mother', 'Mother'))
    name = forms.CharField(100)
    rela_name = forms.ChoiceField(choices=CHOICES)

class UpdateEduForm(forms.Form):
    CHOICES = (
        ('Kindergarden', 'Kindergarden'),
        ('Primary School', 'Primary School'),
        ('Secondary School', 'Secondary School'),
        ('High School', 'High School'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('PhD', 'PhD')
    )
    degree = forms.CharField(widget=forms.Select(choices=CHOICES))
    start = forms.DateField(widget = forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))
    end = forms.DateField(widget = forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))

class AddEduForm(forms.Form):
    CHOICES = (
        ('Kindergarden','Kindergarden'),
        ('Primary School', 'Primary School'),
        ('Secondary School', 'Secondary School'),
        ('High School', 'High School'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('PhD', 'PhD')
    )
    school = forms.CharField()
    degree = forms.CharField(widget=forms.Select(choices=CHOICES))
    date_start = forms.DateField(widget = forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))
    date_end = forms.DateField(widget = forms.SelectDateWidget(years=range(1900, (datetime.now().year)+1)))