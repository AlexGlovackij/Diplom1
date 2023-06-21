from django import forms
from .models import UserBase
from django.contrib.auth.forms import(AuthenticationForm,UserChangeForm,PasswordResetForm,PasswordChangeForm,SetPasswordForm)
from django.contrib.auth.views import LoginView


class UserLoginForm(AuthenticationForm):

    username=forms.CharField(widget=forms.TextInput)
    attrs={'class':'form-control mb-3','placeholder':'Username','id':'login-username'}
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Password',
            'id':'login-pwd',
        }
    ))

    class UserChangeForm(forms.ModelForm):

     email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        #self.fields['email'].required = True

class RegistrationForm(forms.ModelForm):
    
    user_name=forms.CharField(label='Логін', min_length=4,max_length=50,help_text='Required')
    email=forms.EmailField(max_length=100,help_text='Required',error_messages={'required':'Sorry,you will need an email'})
    password=forms.CharField(label='Пароль',widget=forms.PasswordInput)
    password2=forms.CharField(label='Повторіть пароль',widget=forms.PasswordInput)

    class Meta:
        model=UserBase
        fields=('user_name','email',)

    def clean_username(self):
        user_name=self.cleaned_data['user_name'].lower()
        r=UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Користувач з таким іменем вже існує")
        return user_name
    
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Паролі не збігаються')
        return cd['password2'] 
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже використовується')
        return email 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': ''})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': '', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': ''})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        
class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Нажаль ми не можемо знайти дану електронну пошту')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

        