from django.urls import include, path
from django.conf.urls import url
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/add-to-cart/', views.AddToCartApiView.as_view(), name='add-product-to-cart'),
]
