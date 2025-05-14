from django.urls import path
from . import views

urlpatterns = [
    path("", views.shop, name="shop"),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),

]
