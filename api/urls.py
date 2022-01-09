from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework.authtoken import views

import api.views as av


router = routers.DefaultRouter(trailing_slash=False)

router.register('users', av.UserViewSet, 'users')
router.register('wallets', av.WalletViewSet, 'wallet')
router.register('transactions', av.TransactionViewSet, 'transactions')


urlpatterns = [
    path('', include(router.urls)),
    path('token-auth', views.obtain_auth_token, name='api-auth-token'),
]