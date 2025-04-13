from django.contrib import admin
from django.urls import include, path
# from hed import views, edituser
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('user/', views.checkService),
#     path('useredit/', edituser.editcheckService),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hed.urls')),
]
