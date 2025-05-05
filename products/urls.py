from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttributeViewSet, AttributeValueViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'attributes', AttributeViewSet)
router.register(r'attribute-values', AttributeValueViewSet)
router.register(r'products', ProductViewSet)
#router.register(r'variants', ProductVariantViewSet)


urlpatterns = [
    path('', include(router.urls)),
]