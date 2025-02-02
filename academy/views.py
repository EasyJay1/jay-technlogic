from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Max, Min, Count
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from accounts.models import Student
from accounts.models import User, Student
from result.models import TakenCourse
from accounts.decorators import staff_required, student_required
from .forms import (
    ProgramForm, CourseAddForm, CourseAllocationForm,
    EditCourseAllocationForm, UploadFormFile, UploadFormVideo
)
from .models import Program, Course, CourseAllocation, Upload, UploadVideo

from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from .models import Program, Course

# ########################################################
# Program views
# ########################################################
@login_required
def program_view(request):
    programs = Program.objects.all()

    program_filter = request.GET.get('program_filter')
    if program_filter:
        programs = Program.objects.filter(title__icontains=program_filter)

    return render(request, 'course/program_list.html', {
        'title': "Programs | DjangoSMS",
        'programs': programs,
    })


@login_required
@staff_required
def program_add(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, request.POST.get('title') + ' program has been created.')
            return redirect('programs')
        else:
            messages.error(request, 'Correct the error(S) below.')
    else:
        form = ProgramForm()

    return render(request, 'course/program_add.html', {
        'title': "Add Program | DjangoSMS",
        'form': form,
    })



@login_required
def program_detail(request, pk):
    # Retrieve the program and its associated courses
    program = get_object_or_404(Program, pk=pk)
    courses = Course.objects.filter(program_id=pk)

    # Get search parameters from the URL query parameters
    level = request.GET.get('level')
    session = request.GET.get('session')
    course_name = request.GET.get('name')

    # Apply filters based on search parameters
    if level:
        courses = courses.filter(level=level)
    if session:
        courses = courses.filter(year=session)
    if course_name:
        courses = courses.filter(Q(title__icontains=course_name))

    # Calculate total credits for filtered courses
    credits = courses.aggregate(Sum('credit'))

    # Pagination
    paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    courses = paginator.get_page(page)

    # Prepare context data for rendering
    context = {
        'title': program.title,
        'program': program,
        'courses': courses,
        'credits': credits,
        "filter_form": CourseFilterForm(request.GET),  # Include the filter form in the context
    }

    # Render the template with context data
    return render(request, 'course/program_single.html', context)


@login_required
@staff_required
def program_edit(request, pk):
    program = Program.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, str(request.POST.get('title')) + ' program has been updated.')
            return redirect('programs')
    else:
        form = ProgramForm(instance=program)

    return render(request, 'course/program_add.html', {
        'title': "Edit Program | DjangoSMS",
        'form': form
    })


@login_required
@staff_required
def program_delete(request, pk):
    program = Program.objects.get(pk=pk)
    title = program.title
    program.delete()
    messages.success(request, 'Program ' + title + ' has been deleted.')

    return redirect('programs')
# ########################################################

# ########################################################
# Course views
# ########################################################
@login_required
def course_single(request, slug):
    course = Course.objects.get(slug=slug)
    files = Upload.objects.filter(course__slug=slug)
    videos = UploadVideo.objects.filter(course__slug=slug)

    # lecturers = User.objects.filter(allocated_lecturer__pk=course.id)
    lecturers = CourseAllocation.objects.filter(courses__pk=course.id)

    return render(request, 'course/course_single.html', {
        'title': course.title,
        'course': course,
        'files': files,
        'videos': videos,
        'lecturers': lecturers,
        'media_url': settings.MEDIA_ROOT,
    }, )


@login_required
@staff_required
def course_add(request, pk):
    users = User.objects.all()
    if request.method == 'POST':
        form = CourseAddForm(request.POST)
        course_name = request.POST.get('title')
        course_code = request.POST.get('code')
        if form.is_valid():
            form.save()
            messages.success(request, (course_name + '(' + course_code + ')' + ' has been created.'))
            return redirect('program_detail', pk=request.POST.get('program'))
        else:
            messages.error(request, 'Correct the error(s) below.')
    else:
        form = CourseAddForm(initial={'program': Program.objects.get(pk=pk)})

    return render(request, 'course/course_add.html', {
        'title': "Add Course | DjangoSMS",
        'form': form, 'program': pk, 'users': users
    }, )


@login_required
@staff_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseAddForm(request.POST, instance=course)
        course_name = request.POST.get('title')
        course_code = request.POST.get('code')
        if form.is_valid():
            form.save()
            messages.success(request, (course_name + '(' + course_code + ')' + ' has been updated.'))
            return redirect('program_detail', pk=request.POST.get('program'))
        else:
            messages.error(request, 'Correct the error(s) below.')
    else:
        form = CourseAddForm(instance=course)

    return render(request, 'course/course_add.html', {
        'title': "Edit Course | DjangoSMS",
        # 'form': form, 'program': pk, 'course': pk
        'form': form
    }, )


@login_required
@staff_required
def course_delete(request, slug):
    course = Course.objects.get(slug=slug)
    # course_name = course.title
    course.delete()
    messages.success(request, 'Course ' + course.title + ' has been deleted.')

    return redirect('program_detail', pk=course.program.id)
# ########################################################


# ########################################################
# Course Allocation
# ########################################################
@method_decorator([login_required], name='dispatch')
class CourseAllocationFormView(CreateView):
    form_class = CourseAllocationForm
    template_name = 'course/course_allocation_form.html'

    def get_form_kwargs(self):
        kwargs = super(CourseAllocationFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # if a staff has been allocated a course before update it else create new
        lecturer = form.cleaned_data['lecturer']
        selected_courses = form.cleaned_data['courses']
        courses = ()
        for course in selected_courses:
            courses += (course.pk,)
        # print(courses)

        try:
            a = CourseAllocation.objects.get(lecturer=lecturer)
        except:
            a = CourseAllocation.objects.create(lecturer=lecturer)
        for i in range(0, selected_courses.count()):
            a.courses.add(courses[i])
            a.save()
        return redirect('course_allocation_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Assign Course | DjangoSMS"
        return context


@login_required
def course_allocation_view(request):
    allocated_courses = CourseAllocation.objects.all()
    return render(request, 'course/course_allocation_view.html', {
        'title': "Course Allocations | DjangoSMS",
        "allocated_courses": allocated_courses
    })


@login_required
@staff_required
def edit_allocated_course(request, pk):
    allocated = get_object_or_404(CourseAllocation, pk=pk)
    if request.method == 'POST':
        form = EditCourseAllocationForm(request.POST, instance=allocated)
        if form.is_valid():
            form.save()
            messages.success(request, 'course assigned has been updated.')
            return redirect('course_allocation_view')
    else:
        form = EditCourseAllocationForm(instance=allocated)

    return render(request, 'course/course_allocation_form.html', {
        'title': "Edit Course Allocated | DjangoSMS",
        'form': form, 'allocated': pk
    }, )


@login_required
@staff_required
def deallocate_course(request, pk):
    course = CourseAllocation.objects.get(pk=pk)
    course.delete()
    messages.success(request, 'successfully deallocate!')
    return redirect("course_allocation_view")
# ########################################################


# ########################################################
# File Upload views
# ########################################################
@login_required
@staff_required
def handle_file_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, {'course': course})
        # file_name = request.POST.get('name')
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('title') + ' has been uploaded.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormFile()
    return render(request, 'upload/upload_file_form.html', {
        'title': "File Upload | DjangoSMS",
        'form': form, 'course': course
    })


@login_required
@staff_required
def handle_file_edit(request, slug, file_id):
    course = Course.objects.get(slug=slug)
    instance = Upload.objects.get(pk=file_id)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        # file_name = request.POST.get('name')
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('title') + ' has been updated.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormFile(instance=instance)

    return render(request, 'upload/upload_file_form.html', {
        'title': instance.title,
        'form': form, 'course': course})


def handle_file_delete(request, slug, file_id):
    file = Upload.objects.get(pk=file_id)
    # file_name = file.name
    file.delete()

    messages.success(request, (file.title + ' has been deleted.'))
    return redirect('course_detail', slug=slug)

# ########################################################
# Video Upload views
# ########################################################
@login_required
@staff_required
def handle_video_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = UploadFormVideo(request.POST, request.FILES, {'course': course})
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('title') + ' has been uploaded.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormVideo()
    return render(request, 'upload/upload_video_form.html', {
        'title': "Video Upload | DjangoSMS",
        'form': form, 'course': course
    })


@login_required
# @staff_required
def handle_video_single(request, slug, video_slug):
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    return render(request, 'upload/video_single.html', {'video': video})


@login_required
@staff_required
def handle_video_edit(request, slug, video_slug):
    course = Course.objects.get(slug=slug)
    instance = UploadVideo.objects.get(slug=video_slug)
    if request.method == 'POST':
        form = UploadFormVideo(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, (request.POST.get('title') + ' has been updated.'))
            return redirect('course_detail', slug=slug)
    else:
        form = UploadFormVideo(instance=instance)

    return render(request, 'upload/upload_video_form.html', {
        'title': instance.title,
        'form': form, 'course': course})


def handle_video_delete(request, slug, video_slug):
    video = get_object_or_404(UploadVideo, slug=video_slug)
    # video = UploadVideo.objects.get(slug=video_slug)
    video.delete()

    messages.success(request, (video.title + ' has been deleted.'))
    return redirect('course_detail', slug=slug)
# ########################################################
from accounts.forms import StudentFilterForm

# ########################################################
# Course Registration
# ########################################################
@login_required
def course_registration(request):
    filter_form = StudentFilterForm()
    if request.method == 'POST':
        payment = request.POST.get('payment')
        if payment:
            student = Student.objects.get(student__pk=request.user.id)
            student.payment = payment
            student.save()
            messages.success (request, 'Payment' +" "+ payment)
            return redirect('course_registration')
        else:
            messages.success(request, 'Welcome')

        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # Remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            student = Student.objects.get(student__pk=request.user.id)
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.create(student=student, course=course)
            obj.save()
        messages.success(request, 'Courses Registered Successfully!')
        return redirect('course_registration')
    else:
        student = get_object_or_404(Student, student__id=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=request.user.id)
        t = ()
        for i in taken_courses:
            t += (i.course.pk,)
        current_semester = Semester.objects.get(is_current_semester=True)

        courses = Course.objects.filter(program__pk=student.department.id, level=student.level, semester=current_semester
        ).exclude(id__in=t).order_by('year')
        all_courses = Course.objects.filter(level=student.level, program__pk=student.department.id)

        no_course_is_registered = False  # Check if no course is registered
        all_courses_are_registered = False

        registered_courses = Course.objects.filter(level=student.level).filter(id__in=t)
        if registered_courses.count() == 0:  # Check if the number of registered courses is 0
            no_course_is_registered = True

        if registered_courses.count() == all_courses.count():
            all_courses_are_registered = True

        total_first_semester_credit = 0
        total_sec_semester_credit = 0
        total_registered_credit = 0
        for i in courses:
            if i.semester == "First":
                total_first_semester_credit += int(i.credit)
            if i.semester == "Second":
                total_sec_semester_credit += int(i.credit)
        for i in registered_courses:
            total_registered_credit += int(i.credit)
        context = {
            "is_calender_on": True,
            "all_courses_are_registered": all_courses_are_registered,
            "no_course_is_registered": no_course_is_registered,
            "current_semester": current_semester,
            "courses": courses,
            "total_first_semester_credit": total_first_semester_credit,
            "total_sec_semester_credit": total_sec_semester_credit,
            "registered_courses": registered_courses,
            "total_registered_credit": total_registered_credit,
            "student": student,
            "filter_form": filter_form,
        }
        return render(request, 'course/course_registration.html', context)

@login_required
def course_drop(request):
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            student = Student.objects.get(student__pk=request.user.id)
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.get(student=student, course=course)
            obj.delete()
            messages.success(request, 'Successfully Dropped!')
        return redirect('course_registration')
# ########################################################


@login_required
def user_course_list(request):
    if request.user.is_staff:
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id)

        return render(request, 'course/user_course_list.html', {'courses': courses})

    elif request.user.is_student:
        student = Student.objects.get(student__pk=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=student.student.id)
        courses = Course.objects.filter(level=student.level).filter(program__pk=student.department.id)

        return render(request, 'course/user_course_list.html', {
            'student': student,
            'taken_courses': taken_courses,
            'courses': courses
        })

    else:
        return render(request, 'course/user_course_list.html')


#############################################################################################
# ########################################################
# Session
# ########################################################
@login_required
@staff_required
def session_list_view(request):
    """ Show list of all sessions """
    sessions = Session.objects.all().order_by('-is_current_session', '-session')
    return render(request, 'app/session_list.html', {"sessions": sessions})


@login_required
@staff_required
def session_add_view(request):
    """ check request method, if POST we add session otherwise show empty form """
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_session')  # returns string of 'True' if the user selected Yes
            print(data)
            if data == 'true':
                sessions = Session.objects.all()
                if sessions:
                    for session in sessions:
                        if session.is_current_session == True:
                            unset = Session.objects.get(is_current_session=True)
                            unset.is_current_session = False
                            unset.save()
                    form.save()
                else:
                    form.save()
            else:
                form.save()
            messages.success(request, 'Session added successfully. ')
            return redirect('session_list')

    else:
        form = SessionForm()
    return render(request, 'app/session_update.html', {'form': form})


@login_required
@staff_required
def session_update_view(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        data = form.data.get('is_current_session')
        if data == 'true':
            sessions = Session.objects.all()
            if sessions:
                for session in sessions:
                    if session.is_current_session == True:
                        unset = Session.objects.get(is_current_session=True)
                        unset.is_current_session = False
                        unset.save()

            if form.is_valid():
                form.save()
                messages.success(request, 'Session updated successfully. ')
                return redirect('session_list')
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, 'Session updated successfully. ')
                return redirect('session_list')

    else:
        form = SessionForm(instance=session)
    return render(request, 'app/session_update.html', {'form': form})


@login_required
@staff_required
def session_delete_view(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if session.is_current_session:
        messages.error(request, "You cannot delete current session")
        return redirect('session_list')
    else:
        session.delete()
        messages.success(request, "Session successfully deleted")
    return redirect('session_list')


# ########################################################


# ########################################################
# Semester
# ########################################################
@login_required
@staff_required
def semester_list_view(request):
    semesters = Semester.objects.all().order_by('-is_current_semester', '-semester')
    return render(request, 'app/semester_list.html', {"semesters": semesters, })


@login_required
@staff_required
def semester_add_view(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_semester')  # returns string of 'True' if the user selected Yes
            if data == 'True':
                semester = form.data.get('semester')
                ss = form.data.get('session')
                session = Session.objects.get(pk=ss)
                try:
                    if Semester.objects.get(semester=semester, session=ss):
                        messages.error(request, semester + " semester in " + session.session + " session already exist")
                        return redirect('add_semester')
                except:
                    semesters = Semester.objects.all()
                    sessions = Session.objects.all()
                    if semesters:
                        for semester in semesters:
                            if semester.is_current_semester == True:
                                unset_semester = Semester.objects.get(is_current_semester=True)
                                unset_semester.is_current_semester = False
                                unset_semester.save()
                        for session in sessions:
                            if session.is_current_session == True:
                                unset_session = Session.objects.get(is_current_session=True)
                                unset_session.is_current_session = False
                                unset_session.save()

                    new_session = request.POST.get('session')
                    set_session = Session.objects.get(pk=new_session)
                    set_session.is_current_session = True
                    set_session.save()
                    form.save()
                    messages.success(request, 'Semester added successfully.')
                    return redirect('semester_list')

            form.save()
            messages.success(request, 'Semester added successfully. ')
            return redirect('semester_list')
    else:
        form = SemesterForm()
    return render(request, 'app/semester_update.html', {'form': form})


@login_required
@staff_required
def semester_update_view(request, pk):
    semester = Semester.objects.get(pk=pk)
    if request.method == 'POST':
        if request.POST.get(
                'is_current_semester') == 'True':  # returns string of 'True' if the user selected yes for 'is current semester'
            unset_semester = Semester.objects.get(is_current_semester=True)
            unset_semester.is_current_semester = False
            unset_semester.save()
            unset_session = Session.objects.get(is_current_session=True)
            unset_session.is_current_session = False
            unset_session.save()
            new_session = request.POST.get('session')
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                set_session = Session.objects.get(pk=new_session)
                set_session.is_current_session = True
                set_session.save()
                form.save()
                messages.success(request, 'Semester updated successfully !')
                return redirect('semester_list')
        else:
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                form.save()
                return redirect('semester_list')

    else:
        form = SemesterForm(instance=semester)
    return render(request, 'app/semester_update.html', {'form': form})


@login_required
@staff_required
def semester_delete_view(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if semester.is_current_semester:
        messages.error(request, "You cannot delete current semester")
        return redirect('semester_list')
    else:
        semester.delete()
        messages.success(request, "Semester successfully deleted")
    return redirect('semester_list')


# ########################################################


# from django.shortcuts import render_to_response
# from django.template import RequestContext

# def handler404(request, exception, template_name="common/404.html"):
#     response = render_to_response("common/404.html")
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render_to_response('common/500.html', {}, context_instance=RequestContext(request))
#     response.status_code = 500

#     return response


# def handler400(request, exception, template_name="common/400.html"):
#     response = render_to_response('common/400.html', context_instance=RequestContext(request))
#     response.status_code = 400

#     return response
