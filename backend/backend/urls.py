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
from django.urls import path

# from customers import views
from django.conf.urls import url
from gallery import views
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    url(r'^getuser$', views.get_user),
    url(r'^signup$', views.user_signup),
    url(r'^login$', views.user_login),
    url(r'^logout$', views.user_logout),

    path('getimage/', views.get_image),
    # path('getuserimage/<int:user_id>', views.get_imgs_owned_by_user),
    path('gettags/', views.get_tags),
    path('api/upsert', views.upsert_image),
    path('api/updateuser', views.update_user),
    path('api/updateavatar', views.update_avatar),


] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# url(r'^api/customers/$', views.customers_list),
# url(r'^api/customers/(?P<pk>[0-9]+)$', views.customers_detail),
# url(r'^api/gallery/(?P<pageNo>[0-9]+)$', views.image_page),
