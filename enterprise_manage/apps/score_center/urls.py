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


router.register(r'score-people', ScorePeopleViewSet, base_name="score-people")
router.register(r'list-score', ListScoreViewSet, base_name="list-score")
router.register(r'score-project', ScoreProjectViewSet, base_name="score-project")
router.register(r'score', ScoreViewSet, base_name="score")
router.register(r'result-order', ResultOrderViewSet, base_name="result-order")
router.register(r'project-1', Project_1, base_name="project-1")
router.register(r'project-2', Project_2, base_name="project-2")
router.register(r'project-3', Project_3, base_name="project-3")
router.register(r'project-4', Project_4, base_name="project-4")
router.register(r'project-5', Project_5, base_name="project-5")
router.register(r'project-6', Project_6, base_name="project-6")




urlpatterns = [
    path(r'', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
