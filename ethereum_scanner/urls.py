"""ethereum_scanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from rest_framework_mongoengine.routers import SimpleRouter

from app_auth.views import ApiKeyViewSet
from app_tx_api.views import GetTxListView

router = SimpleRouter()
router.register(r'txs', GetTxListView, base_name='txs')
router.register(r'api-key', ApiKeyViewSet, base_name='api-key')

urlpatterns = router.urls

urlpatterns += [
    url(r'^admin/', admin.site.urls),
]
