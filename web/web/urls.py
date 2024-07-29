from django.contrib import admin
from django.urls import path
from webapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('upload/', views.upload, name='upload'),
    path('open_camera/', views.open_camera, name='open_camera'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
