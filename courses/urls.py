from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('application/create/', views.create_application, name='create_application'),
    path('cabinet/review/<int:application_id>/', views.add_review, name='add_review'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('admin/applications/', views.admin_applications, name='admin_applications'),
    path('admin/change-status/<int:application_id>/', views.change_status, name='change_status'),
]