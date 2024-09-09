from django.contrib import admin
from .models import Program, Course, CourseAllocation, Upload
from result.models import TakenCourse


def register_courses_for_students(modeladmin, request, queryset):
    # The 'queryset' parameter contains the selected courses in the admin interface.

    for course in queryset:
        # Access the student associated with the selected course.
        student = course.student  # Assuming 'student' is the name of the ForeignKey field.

        # Register the course for the student.
        TakenCourse.objects.create(student=student, course=course)


register_courses_for_students.short_description = "Register selected courses for students"


class CourseAdmin(admin.ModelAdmin):
    actions = [register_courses_for_students]


admin.site.register(Course, CourseAdmin)

admin.site.register(Program)
admin.site.register(CourseAllocation)
admin.site.register(Upload)
