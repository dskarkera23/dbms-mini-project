from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, user_views, trainer_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('base/', views.BASE, name='base'),

                  path('', views.LOGIN, name='login'),
                  path('signup/', views.SIGNUP, name='signup'),
                  path('doLogin', views.doLogin, name='doLogin'),
                  path('doLogout', views.doLogout, name='doLogout'),
                  path('doSignup', views.doSignup, name='doSignup'),

                  path('User/home', user_views.HOME, name='user_home'),
                  path('Trainer/home', trainer_views.HOME, name='trainer_home'),
                  path('dashboard/', user_views.dashboard, name='dashboard'),
                  path('get_bmi_graph_data/', user_views.get_bmi_graph_data, name='get_bmi_graph_data'),


                  path('profile', views.PROFILE, name='profile'),
                  path('profile/update', views.PROFILE_UPDATE, name='profile_update'),
                  path('select_trainer/', views.select_trainer, name='select_trainer'),

                  path('User/log/food_log', user_views.FOOD_LOG, name='food_log'),
                  path('User/log/log_food', user_views.log_food, name='log_food'),

                  path('User/log/exe_log', user_views.EXE_LOG, name='exe_log'),
                  path('User/log/log_exercise', user_views.log_exercise, name='log_exercise'),

                  path('User/log/bmi_log', user_views.log_bmi, name='bmi_log'),

                  path('trainer_dashboard/', trainer_views.trainer_dashboard, name='trainer_dashboard'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
