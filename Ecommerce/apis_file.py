from django.urls import path, include

urlpatterns = [
    path('products/', include("products.api.urls")),
    path('categories/', include("products.api.urls")),
    path('user/', include("users.api.urls")),
    path('cart/', include("carts.api.urls")),
    path('order/', include("orders.api.urls")),


]
