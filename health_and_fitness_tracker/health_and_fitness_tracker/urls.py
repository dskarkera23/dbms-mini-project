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
                  path('doLogout', views.doLogout, name='doLogout'),

                  path('User/home', user_views.HOME, name='user_home'),

                  #path('User/log/exelog', user_views.EXE_LOG, name='exe_log'),

                  path('profile', views.PROFILE, name='profile'),
                  path('profile/update', views.PROFILE_UPDATE, name='profile_update'),

                  path('User/log/food_log', user_views.FOOD_LOG, name='food_log'),
                  path('User/log/log_food', user_views.log_food, name='log_food'),




              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
