from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
urlpatterns=[
    path('',views.category,name='category'),
    path('store/<int:id>', views.store, name="store"),
    path('cart',views.cart, name="cart"),
    path('addtocart/<int:id>',views.add_to_cart, name="addtocart"),
    path('view/<int:id>',views.view_item, name="view"),
    path('destroy/<int:id>',views.destroy, name="destroy"),
    path('checkout',views.checkout,name="checkout"),
    path('handle_request',views.handle_request,name="handle_request"),
    path('login',views.loginn,name="login"),
    path('logout/',views.logoutt,name="logout"),
    path('register',views.register,name="register"),
    path('increase_quantity/<int:id>',views.increase_item_quantity,name="increase_quantity"),
    path('decrease_quantity/<int:id>',views.decrease_item_quantity,name="decrease_quantity"),
    path('increasequantity/<int:id>',views.increase_quantity,name="increasequantity"),
    path('decreasequantity/<int:id>',views.decrease_quantity,name="decreasequantity"),
    path('profile',views.profile,name="profile"),
    path('update_profile',views.update_profile, name="update_profile"),
    path('buy/<int:id>',views.buynow, name="buy"),
    path('buy/product_handler',views.product_handler,name="product_handler"),
    path('verify/<auth_token>',views.verify,name="verify"),
    path('cancelled',views.cancelled,name="cancelled"),
    path('cancel_order/<int:id>',views.cancel_order, name="cancel_order"),
    path('order_status/<int:id>',views.order_status,name="order_status"),
    path('view_order',views.view_order,name="view_order"),

    path('password_reset', 
    auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
    name="reset_password"),

    path('password_reset_done',
    auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>', 
    auth_views.PasswordResetConfirmView.as_view(template_name="password_confirm.html"), 
    name="password_reset_confirm"),
   
    path('password_reset_complete', 
    auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
    name="password_reset_complete"),
]