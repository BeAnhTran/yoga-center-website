from django.urls import include, path
from django.conf.urls import url
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/add-to-cart/', views.AddToCartApiView.as_view(),
         name='add-product-to-cart'),
    path('<int:pk>/change-product-quantity-in-cart/', views.ChangeProductCartQuantityApiView.as_view(),
         name='change-product-quantity-in-cart'),
    path('<int:pk>/remove-product-out-of-cart/', views.RemoveProductOutOfCartView.as_view(),
         name='remove-product-out-of-cart'),
]
