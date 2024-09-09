from datetime import datetime
import random
from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import ASCIIUsernameValidator


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) |
                         Q(first_name__icontains=query) |
                         Q(last_name__icontains=query) |
                         Q(email__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures/%y/%m/%d/', default='default.png', null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_dep_head = models.BooleanField(default=False)

    username_validator = ASCIIUsernameValidator()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    @property
    def get_full_name(self):
        full_name = self.first_name + " " + self.last_name if self.first_name and self.last_name else self.username
        return full_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.is_superuser:
            return "Admin"
        elif self.is_staff:
            return "Staff"
        elif self.is_student:
            return "Student"
        return "Client"

    def get_picture(self):
        try:
            return self.picture.url
        except:
            return settings.MEDIA_URL + 'default.png'

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + 'default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)


class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(level__icontains=query) |
                         Q(certificate__icontains=query) |
                         Q(session__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


class Student(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Admission_id = models.CharField(max_length=20, blank=True, unique=True)
    certificate = models.ForeignKey('academy.Program', on_delete=models.CASCADE, null=True)
    certificate_course = models.ForeignKey('academy.Course', on_delete=models.CASCADE, null=True)

    objects = StudentManager()

    def __str__(self):
        return str(self.student)

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)

    def generate_unique_admission_number(self):
        while True:
            random_number = random.randint(10000, 99999)
            current_year = datetime.now().year
            admission_number = f"JAY/{random_number}/{current_year}"
            if not Student.objects.filter(Admission_id=admission_number).exists():
                return admission_number

    def save(self, *args, **kwargs):
        if not self.Admission_id:
            self.Admission_id = self.generate_unique_admission_number()
        super().save(*args, **kwargs)


class Message(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    students = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    certificates = models.ForeignKey('academy.Program', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    @classmethod
    def unread_count(cls, student, certificate):
        return cls.objects.filter(students=student, certificates=certificate, is_read=False).count()

    def __str__(self):
        return f"{self.title} read by {self.students} is {self.is_read}"


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s {self.__class__.__name__}"


class DepartmentHead(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey('academy.Program', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)
