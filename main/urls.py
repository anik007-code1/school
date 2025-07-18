from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('notices/', views.notices, name='notices'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('teachers/', views.teachers, name='teachers'),
    path('committee/', views.committee, name='committee'),
    path('headmaster/', views.headmaster, name='headmaster'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/image/<int:image_id>/', views.gallery_image_detail, name='gallery_detail'),
    path('contact/', views.contact, name='contact'),
]
