from django.contrib import admin
from django.urls import include, path
from hed import views, edituser, eventhands
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.checkService),
    path('useredit/', edituser.editcheckService),
    path('eventapi/', eventhands.eventapi)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)