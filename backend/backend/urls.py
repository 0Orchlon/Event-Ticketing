from django.contrib import admin
from django.urls import include, path
from hed import views, edituser, eventhands
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.checkService),
    path('useredit/', edituser.editcheckService),
    path('eventapi/', eventhands.EventService)
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('hed.urls')),
# ]
