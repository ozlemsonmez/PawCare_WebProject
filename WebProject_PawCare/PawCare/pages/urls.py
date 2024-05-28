from django.urls import path
from .views import (
    HomeView, KullaniciPageView, GirisPageView, 
    KayitPageView, IletisimPageView, VetPageView, 
    IlacPageView, CikisYapView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('kullanici/', KullaniciPageView.as_view(), name='kullaniciPage'),
    path('giris/', GirisPageView.as_view(), name='girisPage'),
    path('kayit/', KayitPageView.as_view(), name='kayitPage'),
    path('iletisim/', IletisimPageView.as_view(), name='iletisimPage'),
    path('vet/', VetPageView.as_view(), name='vetPage'),
    path('ilac/', IlacPageView.as_view(), name='ilacPage'),
    path('cikis/', CikisYapView.as_view(), name='cikisYap'),
]