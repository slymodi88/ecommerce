from rest_framework.routers import DefaultRouter
from carts.api import views

router = DefaultRouter()
router.register('', views.CartApi, basename='cart')
urlpatterns = router.urls



