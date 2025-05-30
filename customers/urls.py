from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet,  BuyNowAPIView, CartAPIView, HasNewNotificationsView, MarkAllNotificationsSeenView, LatestCartItemView, UserNotificationsView, AdminCustomerPoolCreate

router = DefaultRouter()
#router.register(r'buy-now', BuyNpwViewSet, basename="butnow")
router.register(r'cart', CartViewSet)

#router.register(r'variants', ProductVariantViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('buy-now/', BuyNowAPIView.as_view(), name='buy-now'),
    path('carts/', CartAPIView.as_view()),  # POST
    path('carts/<int:cart_id>/', CartAPIView.as_view()),
    path('unseen/notifications/', HasNewNotificationsView.as_view(), name = "unseen-notifications"),
    path('mark-notifications/', MarkAllNotificationsSeenView.as_view(), name = "mark-notifications"),
    path('latest-cart/', LatestCartItemView.as_view(), name = "latest-cart"),
    path('notifications/', UserNotificationsView.as_view(), name = "notifications"),
    path('admin-pool-create/', AdminCustomerPoolCreate.as_view(), name = "pool-creation"),
    
    
]