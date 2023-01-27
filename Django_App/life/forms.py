from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm


# SignUp用フォーム
class RegistForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーネーム')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='もう一度パスワードを入力', widget=forms.PasswordInput())
    class Meta():
        model = Users
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


# login用フォーム
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザーネーム')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())


# バーコードアップデート用フォーム
class BarcodeUpdateForm(forms.Form):
    barcode_image = forms.ImageField(label='画像')


# バーコード入力用フォーム
class BarcodeInputForm(forms.Form):
    barcode = forms.IntegerField(label='数字')
