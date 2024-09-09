from . import views
from django.urls import path
from .views import AppointmentListView, AppointmentCreateView, AppointmentUpdateView, \
    AppointmentDeleteView, download_pdf

urlpatterns = [
    path("", views.home_view, name="index"),
    path("article/<slug:slug>", views.detail, name="detail"),

    path("maintain", views.maintain, name="maintain"),
    path("navslider", views.navslide, name="navslide"),

    path('checkings/', views.create_testimony, name='create_test'),
    path('view-checking/', views.testimony_list, name='test_list'),
    path("terms", views.terms, name="terms"),
    path("privacy", views.privacy, name="privacy"),
    path('download-pdf/', download_pdf, name='download_pdf'),

    path('view', AppointmentListView.as_view(), name='appointment_list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),

]
