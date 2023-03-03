from django import forms
from .models import Users, CategoryModel, BookBarcodeModel, BookModel
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from datetime import date


# SignUp用フォーム
class RegistForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"ユーザーネーム"}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={"placeholder":"メールアドレス"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder":"パスワード"}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder":"もう一度パスワードを入力"}))
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
    username = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"ユーザーネーム"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder":"パスワード"}))


# カテゴリー作成用フォーム
class CategoryAddForm(forms.ModelForm):
    class Meta():
        model = CategoryModel
        fields = ['category_name']
        labels = {'category_name':'カテゴリー'}


# バーコードアップデート用フォーム
class BarcodeUpdateForm(forms.Form):
    barcode_image = forms.ImageField(label='', required=False)


# バーコード入力用フォーム
class BarcodeInputForm(forms.Form):
    barcode = forms.IntegerField(label='', required=False)


# Date入力用
class DateInput(forms.DateInput):
    input_type = 'date'


# 本データ入力用フォーム
class BookAddForm(forms.ModelForm):
    barcode = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(label='タイトル')
    author = forms.CharField(label='著者',required=False)
    price = forms.IntegerField(label='購入金額')
    page_count = forms.IntegerField(label='ページ数')
    image_link = forms.URLField(label='image', widget=forms.URLInput(attrs={"class":"form-img-link"}), required=False)
    image_path = forms.ImageField(label='+', required=False)
    released_at = forms.DateField(label='発売日', widget=DateInput(), required=False)
    purchased_at = forms.DateField(label='購入日', widget=DateInput())
    category = forms.ModelChoiceField(label='カテゴリー', queryset=CategoryModel.objects.none())

    class Meta():
        model = BookBarcodeModel
        fields = ['barcode', 'title', 'author', 'image_link', 'image_path', 'released_at', 'purchased_at', 'page_count', 'category', 'price']

    def __init__(self, *args, **kwargs):
        book = kwargs.pop('book')
        self.base_fields["barcode"].initial = book["barcode"]
        self.base_fields["title"].initial = book["title"]
        self.base_fields["author"].initial = '、'.join(book["author"])
        self.base_fields["price"].initial = book["price"]
        self.base_fields["page_count"].initial = book["page_count"]
        self.base_fields["image_link"].initial = book["image_link"]
        self.base_fields["released_at"].initial = book["released_at"]
        self.base_fields["purchased_at"].initial = date.today()
        self.base_fields["category"].queryset = book["category"]
        self.base_fields["category"].initial = book["category"][0]
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

# ユーザー情報変更用
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'email')

# パスワード変更用
class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
#詳細情報の更新用
class BookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = ['progress', 'evaluation', 'review','cid']
        
        labels = {
            'progress': '進捗状況',
            'evaluation': '評価',
            'review': '',
            'cid': 'カテゴリー',
        }

    def clean_evaluation(self):
        value = self.cleaned_data['evaluation']
        if value >= 6:
            raise forms.ValidationError('5以下の値を入力してください。')
        return value
        
class BookBarcodeForm(forms.ModelForm):
    class Meta:
        model = BookBarcodeModel
        fields = ['title','author','price','page_count','purchased_at','released_at']
        labels = {
            'title':'',
            'author':'',
            'price': '値段',
            'page_count':'ページ数',
            'purchased_at': '購入日',
            'released_at':'発売日',
        }

class BookBarcodeImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = BookBarcodeModel
        fields = ['image']
        labels = {
            'image':'',
        }

    def save(self, commit=True):
        book = super().save(commit=False)
        image = self.cleaned_data.get('image')
        if image:
            book.image_path.delete()  # 既存の画像を削除
            book.image_path = image  # 新しい画像を設定
        if commit:
            book.save()
        return book


