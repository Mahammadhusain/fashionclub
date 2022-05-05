from django.urls import path
from .views import (ShopView,Add_Cart,ShowCart,
removeItem,PlusQuantity,MinusQuantity,
ProfileView,AddressView,OrdersView,OrderShow,
CheckoutView,ProductDetailsView,AllProductView,
UserRegisterView,CahngePassView,SigninView,Userlogout)
from .form import PassResetForm,SetNewPassForm
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('shop/',ShopView,name='shop'),
    path('cart/<int:id>/',Add_Cart,name='cart'),
    path('showcart/',ShowCart,name='showcart'),
    path('removeItem/<int:id>/',removeItem,name='removeItem'),
    path('plusequntity/<int:id>/',PlusQuantity,name='plusequntity'),
    path('minusquantity/<int:id>/',MinusQuantity,name='minusquantity'),
    
    
    path('profile/',ProfileView,name='profile'),
    path('address/',AddressView,name='address'),
    path('changepass/',CahngePassView,name='changepass'),
    path('orders/',OrdersView,name='orders'),
    path('showorders/',OrderShow,name='showorders'),
    path('checkout/',CheckoutView,name='checkout'),
    path('productdetails/<int:id>/',ProductDetailsView,name='productdetails'),
    path('allproducts/',AllProductView,name='allproducts'),



    # Auth Management
    path('',SigninView,name='signin'),
    path('signout/',Userlogout,name='signout'),
    path('signup/',UserRegisterView,name='signup'),


    #Password Reset
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=PassResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=SetNewPassForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),


]
