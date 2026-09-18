from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('search/category', views.search_by_category, name='search_by_category'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='product_list'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact_view, name='contact'),
    path('search/', views.search_by_name, name='search_by_name'),
]
