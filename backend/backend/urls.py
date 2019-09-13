"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django.conf.urls import url
from gallery import views
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    path('api/getuser', views.get_user),
    path('api/signup', views.user_signup),
    path('api/login', views.user_login),
    path('api/logout', views.user_logout),

    path('api/getimage/', views.get_image),
    path('api/gettags', views.get_tags),
    path('api/upsert', views.upsert_image),
    path('api/updateuser', views.update_user),
    path('api/updateavatar', views.update_avatar),

    path('api/searchimage/', views.search_image)

] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# to defer the matching so that /api/uploads or /api/static wouldnt be captured by the template url
urlpatterns += [re_path(r'^(.*)$', TemplateView.as_view(template_name='index.html'))]
