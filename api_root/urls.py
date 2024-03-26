"""api_root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api_rest.views import home, table, change_password, create_user, edit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('table/', table, name='table'),
    path('edit', edit, name='edit-table'),


    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', change_password, name='change_password'),
    path('accounts/create_user', create_user, name='create_user'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)