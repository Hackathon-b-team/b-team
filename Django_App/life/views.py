from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, FormMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from .forms import RegistForm, LoginForm, BarcodeUpdateForm, BarcodeInputForm, BookAddForm
from .models import Users, CategoryModel, BookBarcodeModel, BookModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from PIL import Image
from pyzbar.pyzbar import decode
import numpy
import requests


# SignUp用
class RegistView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

    def form_valid(self, form):
        self.object = form.save()
        response = super().form_valid(form)
        users = Users.objects.get(username=self.object.username)
        CategoryModel.objects.create(uid=users, category_name="本")
        user = self.object
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return response


# login用
class CustumLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


# logout用
class CustumLogoutView(LogoutView):
    pass


# home用
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


# バーコード画像保存
def imageupload(updata, path):
    f = open(path,'wb+')
    for chunk in updata.chunks():
        f.write(chunk)
    f.close()

# バーコード画像解析
def barcodetonumber(img):
    src_img = Image.open(img)
    rate = numpy.arange(0.5, 2.1, 0.1)
    imgs = [src_img.resize((int(src_img.width * i), int(src_img.height * i)), Image.LANCZOS) for i in rate]
    datas = [decode(img) for img in imgs]
    *codes, = filter(lambda x: x, datas)
    if len(codes) > 0:
        # 一番初めにスキャン成功したものを表示
        code = codes[0]
        return code[0][0].decode('utf8')
    else:
        return 'INVARID'


# バーコード用
class BarcodeView(LoginRequiredMixin, TemplateView, FormMixin):
    template_name = 'barcode.html'
    success_url = reverse_lazy('life:add')

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        kwargs.update({
            'barcode_update_form': BarcodeUpdateForm(**self.get_form_kwargs()),
            'barcode_input_form': BarcodeInputForm(**self.get_form_kwargs()),
        })
        return kwargs

    def post(self, request, *args, **kwargs):
        # バーコードアップデート用
        if 'button_send_barcode_update' in request.POST:
            updateform = BarcodeUpdateForm(**self.get_form_kwargs())
            # バリデーション
            if updateform.is_valid():
                return self.form_valid(updateform)
            else:
                return self.form_invalid(updateform)
        # バーコードインプット用
        elif 'button_send_barcode_input' in request.POST:
            inputform = BarcodeInputForm(**self.get_form_kwargs())
            # バリデーション
            if inputform.is_valid():
                return self.form_valid(inputform)
            else:
                return self.form_invalid(inputform)

    def form_valid(self, form):
        barcode = None
        # バーコード取得
        if 'barcode_image' in form.cleaned_data:
            path = f"{settings.MEDIA_ROOT}/barcode/{form.cleaned_data['barcode_image']}"
            imageupload(form.cleaned_data['barcode_image'], path)
            barcode = barcodetonumber(path)
            if barcode == 'INVARID':
                return self.form_invalid(form)
        elif 'barcode' in form.cleaned_data:
            barcode = form.cleaned_data['barcode']
        # バーコードの制限
        if not len(str(barcode))==10 and not len(str(barcode))==13:
            return self.form_invalid(form)
        elif len(str(barcode))==13:
            if not str(barcode).startswith("978"):
                return self.form_invalid(form)
        self.request.session['barcode'] = barcode
        return HttpResponseRedirect(self.get_success_url())


# APIデータ登録用
class BookAddView(LoginRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = BookAddForm
    success_url = reverse_lazy('life:home')

    def get_form_kwargs(self):
        # APIからデータ取得
        barcode = self.request.session['barcode']
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{barcode}"
        book = requests.get(url)
        book_data = book.json()
        # 取得したデータの処理
        title = book_data["items"][0]["volumeInfo"]["title"]
        author = book_data["items"][0]["volumeInfo"]["authors"]
        if "listPrice" in book_data["items"][0]["saleInfo"]:
            price = book_data["items"][0]["saleInfo"]["listPrice"]["amount"]
        else:
            price = 0
        if "pageCount" in book_data["items"][0]["volumeInfo"]:
            page_count = book_data["items"][0]["volumeInfo"]["pageCount"]
        else:
            page_count = 0
        if "imageLinks" in book_data["items"][0]["volumeInfo"]:
            if "thumbnail" in book_data["items"][0]["volumeInfo"]["imageLinks"]:
                image_link = book_data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        else:
            image_link = None
        if "publishedDate" in book_data["items"][0]["volumeInfo"]:
            released_at = book_data["items"][0]["volumeInfo"]["publishedDate"]
        else:
            released_at = None

        regist_book_data= {"barcode":barcode,"title":title,"author":author,"price":price,"page_count":page_count,"image_link":image_link,"released_at":released_at}
        kwargs = super().get_form_kwargs()
        kwargs["book"] = regist_book_data
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.request.session.pop('barcode')
        users = Users.objects.get(id=self.request.user.id)
        cate = CategoryModel.objects.get(uid=self.request.user.id)
        bar = BookBarcodeModel.objects.get(id=self.object.id)
        BookModel.objects.create(uid=users, cid=cate, bid=bar)
        return super().form_valid(form)

