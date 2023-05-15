from django.urls import path
from app import views

urlpatterns = [
    path('',  views.ShopView.as_view(), name='shop'),
    path('diagnose/', views.DiagnoseView.as_view(), name='diagnose'),
    path('introduce/', views.IntroduceView.as_view(), name='introduce'),
    path('fundamental/', views.FundamentalView.as_view(), name='fundamental'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('index/<str:key>', views.IndexListView.as_view(), name='indexlist'),
    path('product/<slug>', views.ItemDetailView.as_view(), name='product'),
    path('additem/<slug>', views.addItem, name='additem'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('removeitem/<slug>', views.removeItem, name='removeitem'),
    path('removesingleitem/<slug>', views.removeSingleItem, name='removesingleitem'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path("form/", views.ContactFormView.as_view(), name='form'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('form-thanks/', views.ThanksView.as_view(), name='form-thanks'),
]