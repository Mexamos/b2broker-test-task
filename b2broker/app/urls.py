from django.urls import include, path
from rest_framework import routers

from app.views import TransactionViewSet, WalletViewSet

router = routers.DefaultRouter()
router.register(r'wallet', WalletViewSet)
router.register(r'transaction', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
