from django.urls import path, include
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, 
    PasswordResetCompleteView, LoginView, LogoutView
    )
from . import views

from .views import (
        profile, profile_single, admin_panel,view_messages, open_message, assemble_payment,
        profile_update, change_password, create_message,
        LecturerListView, StudentListView,
        staff_add_view, edit_staff,
        delete_staff, student_add_view,
        edit_student, delete_student, ClientAdd, validate_username, register
    )
from .forms import EmailValidationOnForgotPassword
from .views import Clientview

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('messages/create/', create_message.as_view(), name='create_message'),

    path('admin_panel/', admin_panel, name='admin_panel'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),

    path('profile/', profile, name='profile'),
    path('profile/<int:id>/detail/', profile_single, name='profile_single'),
    path('setting/', profile_update, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),

    path('lecturers/', LecturerListView.as_view(), name='lecturer_list'),
    path('lecturer/add/', staff_add_view, name='add_lecturer'),
    path('staff/<int:pk>/edit/', edit_staff, name='staff_edit'),
    path('lecturers/<int:pk>/delete/', delete_staff, name='lecturer_delete'),

    path('students/', StudentListView.as_view(), name='student_list'),
    path('student/add/', student_add_view, name='add_student'),
    path('student/<int:pk>/edit/', edit_student, name='student_edit'),
    path('students/<int:pk>/delete/', delete_student, name='student_delete'),

    path('Clients/add/', ClientAdd, name='add_Client'),
    path('view/', Clientview, name='view_Client'),
    path('view_messages/', view_messages, name='view_messages'),

    path('ajax/validate-username/', validate_username, name='validate_username'),
    path('message/<int:message_id>/', open_message, name='open_message'),

    path('signup/', register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # path('add-student/', StudentAddView.as_view(), name='add_student'),

    # path('programs/course/delete/<int:pk>/', course_delete, name='delete_course'),

    # Setting urls
    # path('profile/<int:pk>/edit/', profileUpdateView, name='edit_profile'),
    # path('profile/<int:pk>/change-password/', changePasswordView, name='change_password'),

    # ################################################################
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
    path('assemble-payment/', assemble_payment, name='assemble_payment'),
    path('password-reset/', PasswordResetView.as_view(
         form_class=EmailValidationOnForgotPassword,
         template_name='password_reset_form.html'
     ),
          name='reset'),

     path('password-reset/done/', PasswordResetDoneView.as_view(
         template_name='registration/password_reset_done.html'
     ),
          name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
         template_name='registration/password_reset_confirm.html'
     ),
          name='password_reset_confirm'),
     path('password-reset-complete/', PasswordResetCompleteView.as_view(
         template_name='registration/password_reset_complete.html'
     ),
          name='password_reset_complete')
    # ################################################################
]
