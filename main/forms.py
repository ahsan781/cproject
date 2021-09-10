from django import forms
from django.forms import ModelForm, DateInput
from main.models import *
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from timezone_field import TimeZoneFormField
from django.forms import formset_factory,modelformset_factory

User = get_user_model()







# User  Form
class UserForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

# Login  Form
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')



job = (
    ("Customer 1","Customer 1"),
    ("Project A","Project A"),
    ("Shift Manager","Shift Manager"),
    ("Work site A","Work site A"),
   
)


_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')


class ProfileForm(forms.ModelForm):
  class Meta:
    model = VendorProfile
    fields = ['user','name']



class EventForm(forms.ModelForm):
  # user = forms.ModelChoiceField(queryset=MemberProfile.objects.all())
  note= forms.FileField(required=False)
  tz1 = TimeZoneFormField(choices_display='WITH_GMT_OFFSET')
  date = forms.DateField(
    localize=True,
    widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}),)
  
  class Meta:
    model = ShiftDetail
    widgets = {
       'start_time': forms.TimeInput(attrs={'type': 'time'}),
       'end_time': forms.TimeInput(attrs={'type': 'time'}),
    }
  
    fields= ['title','date','start_time','end_time','location','note','tz1','username','text']




class AddMemberForm(forms.ModelForm):
  class Meta:
    model = EventMember
    fields = ['user']




class AddUserForm(forms.Form):
  class Meta:
    fields = '__all__'


class MultiduplicateForm(forms.Form):
  class Meta:
    fields = '__all__'
