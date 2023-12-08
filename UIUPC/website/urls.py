from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('onlineregistration', views.registration, name='registration'),
    path('faqs', views.faqs, name='faqs'),
    path('events', views.events, name='events'),
    path('<int:e_id>/', views.event_detail, name='event_detail'),
    path('participate/<int:e_id>/', views.participate, name='participate'),
    path('about/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)