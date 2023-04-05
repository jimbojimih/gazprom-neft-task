from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'wiki', views.QuoteViewSet, ) 

urlpatterns = [
        path('', include(router.urls)),
        path('import', views.ImporterView.as_view(), name='import'),
]
#urlpatterns = format_suffix_patterns(urlpatterns)
