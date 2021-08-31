from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.api import views

router = DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('category', views.CategoryViewSet)
urlpatterns = [
    path('', include(router.urls)),

]
