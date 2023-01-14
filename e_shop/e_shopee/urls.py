from . import views
from django.urls import path


app_name = 'e_shopee'

urlpatterns = [
    path('', views.all_product_category, name='all_product_category'),
    path('<slug:c_slug>/', views.all_product_category, name='products_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/', views.all_product_details, name='product_category_details'),
]