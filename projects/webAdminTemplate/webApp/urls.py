from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import ContentViewSet#, MyDRFHTMLView
router = DefaultRouter()
router.register(r'content', ContentViewSet)

#urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)), #/urls/
    path('t2/', views.getDjangoData, name='basePage'),
    path('nokiaStart/', views.funcNokiaStart, name='start'),
    path('nokia4g/', views.funcNokia4g, name='4g'),
    path('nokia3g/', views.funcNokia3g, name='3g'),
    path('nokia2g/', views.funcNokia2g, name='2g'),
    path('nokiaTrx/', views.funcNokiaTrx, name='trx'),
    path('nokiaSsh/', views.funcNokiaSsh, name='ssh'),
    path('nokiaHo24/', views.funcNokiaHo24, name='ho24'),
    path('nokiaPtx3g/', views.funcNokiaPtx3g, name='ptx3g'),
    path('nokiaMassLock/', views.funcNokiaMassLock, name='MassLock'),
    path('ericssonStart/', views.funcEricssonStart, name='erstart'),
    path('ericssonbb4g/', views.funcEricsson4g, name='bb4g'),
    path('ericssonbb3g/', views.funcEricsson3g, name='bb3g'),
    path('ericssonbb3gsix/', views.funcEricsson3gsix, name='bb3gsix'),
    path('ericssonbb2g/', views.funcEricsson2g, name='Ptx3g'),
    path('ericssonlic/', views.funcEricssonLic, name='lic'),
    path('ericssonRet/', views.funcEricssonRet, name='ret'),
]