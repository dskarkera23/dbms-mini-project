from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, user_views, trainer_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('base/', views.BASE, name='base'),

                  path('', views.LOGIN, name='login'),
                  path('doLogin', views.doLogin, name='doLogin'),
                  path('doLogout',views.doLogout, name='doLogout'),

                  path('User/home', user_views.HOME, name='user_home'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
