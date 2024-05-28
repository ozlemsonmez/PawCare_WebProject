from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from django.views import View
from django.contrib.sessions.models import Session

a = "12345"
client = MongoClient("mongodb+srv://melekmbbal:" + a + "@cluster0.1b265hk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["PawCare"]  # database
collection = db["Veterinerler"]  # collection
collection2 = db["kullanicilar"]  # collection
collection3 = db["ilaclar"]  # collection


class MongoService:
    def _init_(self, collection):
        self.collection = collection

    def find_all(self):
        return self.collection.find({})

    def insert_one(self, document):
        self.collection.insert_one(document)


class VeterinerService(MongoService):
    def _init_(self):
        super()._init_(collection)

    def pull_datas(self):
        cursor = self.find_all()
        return [(doc["name"], doc["city"], doc["phone"], doc["address"]) for doc in cursor]


class KullaniciService(MongoService):
    def _init_(self):
        super()._init_(collection2)

    def authorize_save(self, username, no, password):
        self.insert_one({
            "username": username,
            "no": no,
            "password": password
        })

    def authorize_check(self, no, password):
        cursor = self.find_all()
        for document in cursor:
            if document["no"] == no and document["password"] == password:
                return True
        return False


class IlacService(MongoService):
    def _init_(self):
        super()._init_(collection3)

    def pull_datas(self):
        cursor = self.find_all()
        return [(doc["name"], doc["purpose"], doc["frequency"], doc["how"], doc["kullanim"]) for doc in cursor]


class HomeView(View):
    def get(self, request):
        return render(request, 'pages/home.html')


class KullaniciPageView(View):
    def get(self, request):
        username = request.session.get('username', None)
        if username:
            return render(request, 'pages/kullaniciPage.html', {'name': username})
        else:
            return render(request, 'pages/girisPage.html')


class GirisPageView(View):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.kullanici_service = KullaniciService()

    def get(self, request):
        return render(request, 'pages/girisPage.html')

    def post(self, request):
        no = request.POST.get('no', '')
        sifre = request.POST.get('password', '')

        if self.kullanici_service.authorize_check(no, sifre):
            name = collection2.find_one({"no": no})["username"]
            request.session['username'] = name
            return render(request, 'pages/kullaniciPage.html', {'name': name})

        return render(request, 'pages/girisPage.html')


class KayitPageView(View):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.kullanici_service = KullaniciService()

    def get(self, request):
        return render(request, 'pages/kayitPage.html')

    def post(self, request):
        patiAdi = request.POST.get('username', '')
        no = request.POST.get('no', '')
        sifre = request.POST.get('password', '')

        self.kullanici_service.authorize_save(patiAdi, no, sifre)

        return render(request, 'pages/kayitPage.html')


class IletisimPageView(View):
    def get(self, request):
        return render(request, 'pages/iletisimPage.html')


class VetPageView(View):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.veteriner_service = VeterinerService()

    def get(self, request):
        zip_list = self.veteriner_service.pull_datas()
        context = {
            'zip_list': zip_list
        }
        return render(request, 'pages/vetPage.html', context)


class IlacPageView(View):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.ilac_service = IlacService()

    def get(self, request):
        zip_list = self.ilac_service.pull_datas()
        context = {
            'zip_list': zip_list
        }
        return render(request, 'pages/ilacPage.html', context)


class CikisYapView(View):
    def get(self, request):
        if 'username' in request.session:
            del request.session['username']
        return render(request, 'pages/girisPage.html')