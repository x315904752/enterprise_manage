"""enterprise_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import ObtainJSONWebToken

from enterprise_manage.apps.user_center import urls as user_center_urls
from enterprise_manage.apps.score_center import urls as score_center_urls


router = DefaultRouter()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('user-login/', ObtainJSONWebToken.as_view()),
    path(r'', include(router.urls)),
    path(r'user/', include(user_center_urls)),
    path(r'score/', include(score_center_urls))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
