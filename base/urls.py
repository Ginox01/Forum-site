"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path , include

from app.views import homepage , registrazione_user , user_profile , create_section , section , crea_discussione_form
from app.views import discussione , form_post_risposta , users , funzione_cerca , DeletePost

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='homepage'),
    path('search/',funzione_cerca,name='funzione_cerca'),
    path('registrazione/',registrazione_user,name='user_registration'),
    path('user/<str:username>/', user_profile , name='user_profile'),
    path('users/',users,name='users'),
    path('create_section/',create_section,name='new_section'),
    path('section/<int:pk>/',section,name='section'),
    path('section/<int:pk>/crea_discussione_form',crea_discussione_form,name='new-discussion'),
    path('discussione/<int:pk>/',discussione,name='discussion'),
    path('discussione/<int:pk>/form_post_risposta',form_post_risposta,name='answer-form'),
    path('discussione/<int:id>/elimina-post/<int:pk>',DeletePost.as_view(),name='delete')
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)