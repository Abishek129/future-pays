from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttributeViewSet, AttributeValueViewSet, ProductViewSet, SizeCreateAPIView

router = DefaultRouter()
router.register(r'attributes', AttributeViewSet)
router.register(r'attribute-values', AttributeValueViewSet)
router.register(r'products', ProductViewSet)
#router.register(r'variants', ProductVariantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('size-create', SizeCreateAPIView.as_view())
]