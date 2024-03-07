from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('buy-now/', views.buy_now, name='buy_now'),
    path('shop-details/', views.shopDetail, name='shopDetail'),
    path('search/', views.product_search, name='product_search'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
            # admin urls
    path('adminview/',views.adminview,name="adminview"),
    path('create/', views.create_product, name='create_product'),
    path('get_brands/', views.get_brands, name='get_brands'),
]