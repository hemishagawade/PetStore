from django.urls import path
from PetApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.homeFunction),
    path('aboutus',views.aboutusFunction),
    path('contact',views.contactFunction),
    path('login',views.userlogin),
    path('logout',views.userlogout),
    path('register',views.register),
    path('details/<pid>',views.petDetails),
    path('addtocart/<petid>',views.addToCart),
    path('mycart',views.showMyCart),
    path('remove/<cartid>',views.removeFromCart),
    path('confirmorder',views.confirmOrder),
    path('searchby/<val>',views.searchPetsByType),
    path('sort/<dir>',views.sortPetsByPrice),
    path('pricerange',views.priceRange),
    path('makepayment',views.makePayment),
    path('placeorder',views.placeorder),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
