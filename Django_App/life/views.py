from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, FormMixin, ModelFormMixin,DeleteView,UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from .forms import RegistForm, LoginForm, CategoryAddForm, BarcodeUpdateForm, BarcodeInputForm, BookAddForm, UserUpdateForm, PasswordUpdateForm,BookForm, BookBarcodeForm
from .models import Users, CategoryModel, BookBarcodeModel, BookModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages
from PIL import Image
from pyzbar.pyzbar import decode
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy
import requests
import base64


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


class IndexView(TemplateView):
    template_name = "index.html"


class HomeView(LoginRequiredMixin, TemplateView, ModelFormMixin):
    template_name = "home.html"
    form_class = CategoryAddForm
    success_url = reverse_lazy('life:home')
    
    #ユーザーの登録した本だけを表示させるための関数
    def get(self, request, *args, **kwargs):
        bk_list = []
        ca_list = []
        #ログイン中のユーザーのIDを取得
        user_id = request.user.id
        #ユーザーIDが一致する本を探す
        books = BookModel.objects.select_related('bid').filter(uid=user_id)
        bk_list.extend(books)
        #ユーザーIDが一致するカテゴリーを探す
        category = CategoryModel.objects.filter(uid=user_id)
        ca_list.extend(category)
        self.object = None
        context = self.get_context_data(**kwargs)
        context["object_list"] = bk_list
        context["category_list"] = ca_list

        #ブックモデルのIDを送る
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.uid = Users.objects.get(id=self.request.user.id)
        self.object.save()
        return super().form_valid(form)


# 詳細画面用
class DetailView(LoginRequiredMixin, TemplateView):
    template_name = "detail.html"
    
    #URLからnumberを受け取りそのIDの本を表示
    def get(self, request, uuid, *args, **kwargs):
        ctx = {}
        qs_list = []
        qs = BookModel.objects.select_related('bid').filter(uuid=uuid)
        qs_list.extend(qs)
        ctx["object_list"] = qs_list
        return render(request, self.template_name, ctx)


# 詳細画面から削除する
class DetailDeleteView(DeleteView, LoginRequiredMixin, TemplateView):
    template_name = "delete.html"
    model = BookModel
    def get(self, request,pk, *args, **kwargs):
        self.object = self.get_object()
        barcode = self.object.bid
        self.object.delete()
        barcode.delete()
        return redirect("life:home")


#詳細情報を更新
class DetailUpdateView(LoginRequiredMixin, UpdateView):
    model = BookModel
    form_class = BookForm
    success_url = reverse_lazy('life:home')
    template_name = 'book_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['barcode_form'] = BookBarcodeForm(self.request.POST, instance=self.object.bid)
        else:
            context['barcode_form'] = BookBarcodeForm(instance=self.object.bid)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        barcode_form = context['barcode_form']
        if barcode_form.is_valid():
            barcode_form.save()
        return super().form_valid(form)


# バーコード画像保存
def imageupload(updata, path):
    f = open(path, 'wb+')
    for chunk in updata.chunks():
        f.write(chunk)
    f.close()

# バーコード画像解析
def barcodetonumber(img):
    src_img = Image.open(img)
    rate = numpy.arange(0.1, 2.1, 0.1)
    imgs = [src_img.resize(
        (int(src_img.width * i), int(src_img.height * i)), Image.LANCZOS) for i in rate]
    datas = [decode(img) for img in imgs]
    *codes, = filter(lambda x: x, datas)
    if len(codes) > 0:
        # 一番初めにスキャン成功したものを表示
        code = codes[0]
        return code[0][0].decode('utf8')
    else:
        return 'INVALID'


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
            if form.cleaned_data['barcode_image'] == None:
                messages.error(self.request, '10桁or13桁のISBNコードの画像をアップロードしてください')
                return redirect('life:barcode')
            path = f"{settings.MEDIA_ROOT}/barcode/{form.cleaned_data['barcode_image']}"
            imageupload(form.cleaned_data['barcode_image'], path)
            barcode = barcodetonumber(path)
            if barcode == 'INVALID':
                messages.error(self.request, 'バーコード画像をアップロードしてください。もしくは、バーコードと認識できません')
                return redirect('life:barcode')
        elif 'barcode' in form.cleaned_data:
            barcode = form.cleaned_data['barcode']
        # バーコードの制限
        if not len(str(barcode))==10 and not len(str(barcode))==13:
            messages.error(self.request, '10桁or13桁のISBNコードにしてください')
            return redirect('life:barcode')
        elif len(str(barcode))==13:
            if not str(barcode).startswith("978"):
                messages.error(self.request, '13桁の978から始まるISBNコードにしてください')
                return redirect('life:barcode')
        # APIからデータ取得
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{barcode}"
        book = requests.get(url)
        book_data = book.json()
        if "items" not in book_data:
            messages.error(self.request, 'このバーコード番号では、データを取得できませんでした')
            return redirect('life:barcode')
        self.request.session['barcode'] = barcode
        self.request.session['book_data'] = book_data
        return HttpResponseRedirect(self.get_success_url())


# Webカメラでのバーコード取得
class BarcodeCameraView(LoginRequiredMixin, FormView):
    template_name = 'barcode_camera.html'
    form_class = None
    success_url = reverse_lazy('life:add')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # バーコード取得
        data_url = request.POST.get('photo')
        path = f"{settings.MEDIA_ROOT}/barcode/{request.user.username}.png"
        with open(path,"wb") as f:
            f.write(base64.b64decode(data_url.split(',')[1]))
        barcode = barcodetonumber(path)
        if barcode == 'INVALID':
            messages.error(self.request, 'バーコード画像をアップロードしてください。もしくは、バーコードと認識できません')
            return redirect('life:barcode_camera')
        # バーコードの制限
        if not len(str(barcode))==10 and not len(str(barcode))==13:
            messages.error(self.request, '10桁or13桁のISBNコードにしてください')
            return redirect('life:barcode_camera')
        elif len(str(barcode))==13:
            if not str(barcode).startswith("978"):
                messages.error(self.request, '13桁の978から始まるISBNコードにしてください')
                return redirect('life:barcode_camera')
        # APIからデータ取得
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{barcode}"
        book = requests.get(url)
        book_data = book.json()
        if "items" not in book_data:
            messages.error(self.request, 'このバーコード番号では、データを取得できませんでした')
            return redirect('life:barcode_camera')
        self.request.session['barcode'] = barcode
        self.request.session['book_data'] = book_data
        return HttpResponseRedirect(self.get_success_url())


# APIデータ登録用
class BookAddView(LoginRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = BookAddForm
    success_url = reverse_lazy('life:home')

    def get_form_kwargs(self):
        # 取得したデータの処理
        barcode = self.request.session['barcode']
        book_data = self.request.session['book_data']
        title = book_data["items"][0]["volumeInfo"]["title"]
        if "authors" in book_data["items"][0]["volumeInfo"]:
            author = book_data["items"][0]["volumeInfo"]["authors"]
        else:
            author = None
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
        else:
            image_link = None
        if "publishedDate" in book_data["items"][0]["volumeInfo"]:
            released_at = book_data["items"][0]["volumeInfo"]["publishedDate"]
        else:
            released_at = None

        category = CategoryModel.objects.filter(uid=self.request.user.id)
        regist_book_data= {"barcode":barcode,"title":title,"author":author,"price":price,"page_count":page_count,"image_link":image_link,"released_at":released_at,"category":category}
        kwargs = super().get_form_kwargs()
        kwargs["book"] = regist_book_data
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.request.session.pop('barcode')
        self.request.session.pop('book_data')
        category = self.request.POST["category"]
        users = Users.objects.get(id=self.request.user.id)
        cate = CategoryModel.objects.get(id=category)
        bar = BookBarcodeModel.objects.get(id=self.object.id)
        BookModel.objects.create(uid=users, cid=cate, bid=bar)
        return super().form_valid(form)


# お金管理画面用
class MoneyView(LoginRequiredMixin, TemplateView):
    template_name = "money.html"
    
    #ユーザーの登録した本だけを表示させるための関数
    def get(self, request, *args, **kwargs):
        bk_list = []
        month_list = []
        #ログイン中のユーザーのIDを取得
        user_id = request.user.id
        #ユーザーIDが一致する本を探す
        books = BookModel.objects.select_related('bid').filter(uid=user_id).order_by('bid__purchased_at')
        for book in books:
            book.bid.purchased_at_month = book.bid.purchased_at.strftime('%Y/%m')
            book.bid.purchased_at = book.bid.purchased_at.strftime('%m/%d')
        bk_list.extend(books)

        # 月リストの作成
        month_list.append(date.today().strftime('%Y/%m'))
        month = date.today()
        for i in range(1, 12):
            month += relativedelta(months=-1)
            month_list.append(month.strftime('%Y/%m'))

        self.object = None
        context = self.get_context_data(**kwargs)
        context["object_list"] = bk_list
        context["month_list"] = month_list

        return self.render_to_response(context)
    

# username,email変更用
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = 'user_change.html'
    success_url = reverse_lazy('life:user_change')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, '登録内容を変更しました')
        return super().form_valid(form)

# password変更用
class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    model = Users
    form_class = PasswordUpdateForm
    success_url = reverse_lazy('life:password_change')
    template_name = 'password_change.html'

    def form_valid(self, form):
        messages.success(self.request, '登録内容を変更しました')
        return super().form_valid(form)

# User情報表示用
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

# プライバシーポリシーリンク用
class PrivacyView(TemplateView):
    template_name = 'privacy.html'
