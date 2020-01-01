"""mcenter_backstage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter

from enterprise_manage.apps.score_center.views import *

router = DefaultRouter()


router.register(r'score-people', ScorePeopleViewSet, basename="score-people")
router.register(r'list-score', ListScoreViewSet, basename="list-score")
router.register(r'score-project', ScoreProjectViewSet, basename="score-project")
router.register(r'score', ScoreViewSet, basename="score")


urlpatterns = [
    path(r'', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
