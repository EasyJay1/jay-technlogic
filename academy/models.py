from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save
from django.db.models import Q
from datetime import timedelta, datetime

# YEARS choices
current_year = datetime.now().year
YEARS = [(str(year), str(year)) for year in range(current_year, current_year + 1)]  # Next 10 years

class Session(models.Model):
    session = models.CharField(max_length=200, unique=True)
    is_current_session = models.BooleanField(default=False, blank=True, null=True)
    next_session_begins = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.session

class Semester(models.Model):
    is_current_semester = models.BooleanField(default=False, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    next_semester_begins = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.session)

class ProgramManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(summary__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class Program(models.Model):
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(null=True, blank=True)

    objects = ProgramManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('program_detail', kwargs={'pk': self.pk})

class CourseManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(summary__icontains=query) |
                         Q(code__icontains=query) |
                         Q(slug__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class Course(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, unique=True, null=True)
    credit = models.IntegerField(null=True, default=0)
    summary = models.TextField(max_length=200, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    is_elective = models.BooleanField(default=False, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)  # Start date field
    end_date = models.DateField(null=True, blank=True)    # End date field

    objects = CourseManager()

    def __str__(self):
        return "{0} ({1})".format(self.title, self.code)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    @property
    def is_current_semester(self):
        current_semester = Semester.objects.get(is_current_semester=True)
        return self.semester == current_semester.semester

    def calculate_end_date(self, weeks_duration):
        """Calculate the end date excluding Sundays."""
        if self.start_date:
            days_to_add = weeks_duration * 7
            current_date = self.start_date
            while days_to_add > 0:
                current_date += timedelta(days=1)
                if current_date.weekday() != 6:  # Exclude Sundays
                    days_to_add -= 1
            self.end_date = current_date

def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(course_pre_save_receiver, sender=Course)

class CourseAllocation(models.Model):
#    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='allocated_lecturer')
    courses = models.ManyToManyField(Course, related_name='allocated_course')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.lecturer.get_full_name

    def get_absolute_url(self):
        return reverse('edit_allocated_course', kwargs={'pk': self.pk})

class Upload(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='course_files/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    updated_date = models.DateTimeField(auto_now=True, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField(upload_to='course_videos/', validators=[FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])])
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('video_single', kwargs={'slug': self.course.slug, 'video_slug': self.slug})

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)

def video_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(video_pre_save_receiver, sender=UploadVideo)

class CourseOffer(models.Model):
#    dep_head = models.ForeignKey('accounts.DepartmentHead', on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.dep_head)
