from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  GlobalPoolCreateDeleteView, GlobalPoolResetView, CustomerPoolResetView, CustomersPoolResetView, CreateCustomerPool



#router.register(r'variants', ProductVariantViewSet)


urlpatterns = [
    
    path('create-global-pool/', GlobalPoolCreateDeleteView.as_view(), name='create-global-pool'),
    path('rest-global-pool/', GlobalPoolResetView.as_view(), name = "global_pool_reset"),
    path('customer-pool-reset/', CustomerPoolResetView.as_view(), name = "customer-pool-reset" ),
    path('customers-pool-reset/', CustomersPoolResetView.as_view(), name = 'customers-pool-reset'),
    path('customer-pool-create/', CreateCustomerPool.as_view(), name = 'create-customer-pool'),
]