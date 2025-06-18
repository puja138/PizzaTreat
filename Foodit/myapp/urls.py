from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_view, name='home'),            # Home page
    path('about/', views.about_view, name='about'),    # About page
    path('menu/', views.menu_view, name='menu'),       # ✅ Menu page
    path('order/<int:product_id>/', views.order_view, name='order_view'),
    path('place-order/', views.place_order, name='place_order'),

    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/delete/<uuid:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book-table/', views.book_table_view, name='book_table')
]
