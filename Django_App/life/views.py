from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, FormMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from .forms import RegistForm, LoginForm, BarcodeUpdateForm, BarcodeInputForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from PIL import Image
from pyzbar.pyzbar import decode
import numpy
import uuid
import requests

from .models import BookBarcodeModel, BookModel
from django.views.generic import ListView

# SignUp用


class RegistView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

    def form_valid(self, form):
        self.object = form.save()
        response = super().form_valid(form)
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
    template_name = "home.html"
    
    #ユーザーの登録した本だけを表示させるための関数
    def get(self, request, *args, **kwargs):
        ctx = {}
        qs_list = []

        #ログイン中のユーザーのIDを取得
        user_id = request.user.id

        #ユーザーIDが一致する本を探す
        books = BookModel.objects.filter(uid=user_id)

        #本のIDとバーコードのIDが一致するデータをまとめて返す
        for book in books:
            bid = book.bid_id
            qs = BookBarcodeModel.objects.filter(id=bid)
            qs_list.extend(qs)
        ctx["object_list"] = qs_list

        #ブックモデルのIDを送る
        return render(request, self.template_name, ctx)
    
# detail用
class DetailView(LoginRequiredMixin, TemplateView):
    template_name = "detail.html"
    
    #URLからnumberを受け取りそのIDの本を表示
    def get(self, request,number, *args, **kwargs):
        ctx = {}
        qs_list = []
        qs = BookBarcodeModel.objects.filter(id=number)
        qs_list.extend(qs)
        ctx["object_list"] = qs_list
        return render(request, self.template_name, ctx)



# バーコード画像保存
def imageupload(updata, path):
    f = open(path, 'wb+')
    for chunk in updata.chunks():
        f.write(chunk)
    f.close()

# バーコード画像解析


def barcodetonumber(img):
    src_img = Image.open(img)
    rate = numpy.arange(0.5, 2.1, 0.1)
    imgs = [src_img.resize(
        (int(src_img.width * i), int(src_img.height * i)), Image.LANCZOS) for i in rate]
    datas = [decode(img) for img in imgs]
    *codes, = filter(lambda x: x, datas)
    if len(codes) > 0:
        # 一番初めにスキャン成功したものを表示
        code = codes[0]
        return code[0][0].decode('utf8')
    else:
        return 'INVARID'


# バーコード用
class BarcodeView(TemplateView, FormMixin):
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
        if 'barcode_image' in form.cleaned_data:
            path = f"{settings.MEDIA_ROOT}/barcode/{uuid.uuid4().hex}{form.cleaned_data['barcode_image']}"
            imageupload(form.cleaned_data['barcode_image'], path)
            barcode = barcodetonumber(path)
            if barcode == 'INVARID':
                return self.form_invalid(form)
        elif 'barcode' in form.cleaned_data:
            barcode = form.cleaned_data['barcode']
        if not len(str(barcode)) == 10 and not len(str(barcode)) == 13:
            return self.form_invalid(form)
        elif len(str(barcode)) == 13:
            if not str(barcode).startswith("978"):
                return self.form_invalid(form)
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{barcode}"
        book = requests.get(url)
        book_data = book.json()
        title = {"title": book_data["items"][0]["volumeInfo"]["title"]}
        return render(self.request, 'add.html', context=title)
