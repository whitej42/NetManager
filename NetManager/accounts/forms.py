"""

ACCOUNTS/FORMS.PY

* LOGIN FORM
    * LOGGING USER IN

* REGISTER FORM
    * REGISTERING A NEW USER

* PROFILE FORM
    * EDIT ACCOUNT SETTINGS

* CHANGE PASSWORD FORM
    * CHANGING USER PASSWORD

"""

from django import forms
from django.contrib.auth import authenticate, get_user_model


# get django's auth user model
User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid Credentials. Please Try Again')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
        return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Confirm Email Address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            return forms.ValidationError('Email addresses must match')
        email_check = User.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('Account already registered to this email address')
        return super(RegisterForm, self).clean()


class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control detail textbox', 'disabled': 'true'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control detail textbox', 'disabled': 'true'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control detail textbox', 'disabled': 'true'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control detail textbox', 'disabled': 'true'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control textbox'}))
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'form-control textbox'}))

    class Meta:
        model = User
        fields = [
            'password',
            'password2',
        ]

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return super(ChangePasswordForm, self).clean()
