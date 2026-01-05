from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('urls-rest/', include('portfolio.urls')),
    #path('ckeditor/',include('ckeditor_uploader.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', views.contents),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
