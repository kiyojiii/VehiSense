from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customers/', views.customers, name='customers'),
    path('car_brands/', views.car_brands, name='car_brands'),
    path('add_carbrand/', views.add_carbrand, name='add_carbrand'),
    path('edit_carbrand/<int:pk>', views.edit_carbrand, name='edit_carbrand'),
    path('delete_carbrand/<int:pk>', views.delete_carbrand, name='delete_carbrand'),
    path('car_types/', views.car_types, name='car_types'),
    path('add_cartype/', views.add_cartype, name='add_cartype'),
    path('edit_cartype/<int:pk>', views.edit_cartype, name='edit_cartype'),
    path('delete_cartype/<int:pk>', views.delete_cartype, name='delete_cartype'),
    path('all_vehicles/', views.all_vehicles, name='all_vehicles'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('vehicle_details/<int:pk>', views.vehicle_details, name='vehicle_details'),
    path('update_vehicle/<int:pk>', views.update_vehicle, name='update_vehicle'),
    path('delete_vehicle/<int:pk>', views.delete_vehicle, name='delete_vehicle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
