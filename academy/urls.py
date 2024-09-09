from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # Program urls
    path('', program_view, name='programs'),
    path('<int:pk>/detail/', program_detail, name='program_detail'),
    path('add/', program_add, name='add_program'),
    path('<int:pk>/edit/', program_edit, name='edit_program'),
    path('<int:pk>/delete/', program_delete, name='program_delete'),

    # Course urls
    path('course/<slug>/detail/', course_single, name='course_detail'),
    path('<int:pk>/course/add/', course_add, name='course_add'),
    path('course/<slug>/edit/', course_edit, name='edit_course'),
    path('course/delete/<slug>/', course_delete, name='delete_course'),

    # CourseAllocation urls
    path('course/assign/', CourseAllocationFormView.as_view(), name='course_allocation'),
    path('course/allocated/', course_allocation_view, name='course_allocation_view'),
    path('allocated_course/<int:pk>/edit/', edit_allocated_course, name='edit_allocated_course'),
    path('course/<int:pk>/deallocate/', deallocate_course, name='course_deallocate'),

    # File uploads urls
    path('course/<slug>/documentations/upload/', handle_file_upload, name='upload_file_view'),
    path('course/<slug>/documentations/<int:file_id>/edit/', handle_file_edit, name='upload_file_edit'),
    path('course/<slug>/documentations/<int:file_id>/delete/', handle_file_delete, name='upload_file_delete'),

    # Video uploads urls
    path('course/<slug>/video_tutorials/upload/', handle_video_upload, name='upload_video'),
    path('course/<slug>/video_tutorials/<video_slug>/detail/', handle_video_single, name='video_single'),
    path('course/<slug>/video_tutorials/<video_slug>/edit/', handle_video_edit, name='upload_video_edit'),
    path('course/<slug>/video_tutorials/<video_slug>/delete/', handle_video_delete, name='upload_video_delete'),

    # course registration
    path('course/registration', course_registration, name='course_registration'),
    path('course/drop/', course_drop, name='course_drop'),

    path('my_courses/', user_course_list, name="user_course_list"),


    #####################################################################################
    path('session/', session_list_view, name="session_list"),
    path('session/add/', session_add_view, name="add_session"),
    path('session/<int:pk>/edit/', session_update_view, name="edit_session"),
    path('session/<int:pk>/delete/', session_delete_view, name="delete_session"),

    path('semester/', semester_list_view, name="semester_list"),
    path('semester/add/', semester_add_view, name="add_semester"),
    path('semester/<int:pk>/edit/', semester_update_view, name="edit_semester"),
    path('semester/<int:pk>/delete/', semester_delete_view, name="delete_semester"),

]
