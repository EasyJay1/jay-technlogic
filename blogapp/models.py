#import pycountry
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.db.models import Q





BLOGS = "Blogs"
APP = "App"

POST = (
    (BLOGS, "Blogs"),
    (APP, "App"),
)


class CookiesConsent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    consent_given = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class BlogsQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (Q(title__icontains=query) |
                  Q(summary__icontains=query) |
                  Q(posted_as__icontains=query)
                  )
        return self.filter(lookups).distinct()


class BlogsManager(models.Manager):
    def get_queryset(self):
        return BlogsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # NewsAndEvents.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query)


class Blogs(models.Model):
    slug = models.SlugField(unique=True)
    site_link = models.URLField(max_length=500)
    image = models.ImageField(upload_to="media", blank=True, null=True)
    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=5000, blank=True, null=True)
    posted_as = models.CharField(choices=POST, max_length=10)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    is_school = models.BooleanField(default=False)
    is_auto = models.BooleanField(default=False)
    is_shopping = models.BooleanField(default=False)
    is_social = models.BooleanField(default=False)
    is_blockchain = models.BooleanField(default=False)
    is_fashion = models.BooleanField(default=False)
    is_real_estate = models.BooleanField(default=False)
    is_hotel = models.BooleanField(default=False)
    is_others = models.BooleanField(default=False)
    is_appdev = models.BooleanField(default=False)
    is_mobile = models.BooleanField(default=False)
    is_cross = models.BooleanField(default=False)
    is_web = models.BooleanField(default=False)
    is_markerting = models.BooleanField(default=False)
    is_SEO = models.BooleanField(default=False)
    is_SMM = models.BooleanField(default=False)
    is_Emailing = models.BooleanField(default=False)
    is_PPC = models.BooleanField(default=False)
    is_content = models.BooleanField(default=False)
    is_productcat = models.BooleanField(default=False)
    is_ERP = models.BooleanField(default=False)
    is_CRM = models.BooleanField(default=False)
    is_CMS = models.BooleanField(default=False)
    is_CloudB = models.BooleanField(default=False)
    is_BI = models.BooleanField(default=False)
    is_cyber_security = models.BooleanField(default=False)
    is_tips = models.BooleanField(default=False)
    is_guide = models.BooleanField(default=False)

    objects = BlogsManager()

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug} )

    def __str__(self):
        return self.title
# Create your models here.

class Comment(models.Model):
    body = models.TextField()
    user = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add = True)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="comments")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.body

class Appointment(models.Model):
    COMMUNICATION_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('google_meet', 'Google Meet'),
        ('easy_jay_site', 'Easy Jay Site'),
        ('zoom', 'Zoom'),
        ('skype', 'Skype'),
        ('phone_call', 'Phone Call'),
        ('email', 'Email'),
        ('on_site', 'On Site'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_appointments')
 #   location_choices = [(country.name, country.name) for country in pycountry.countries]
  #  location = models.CharField(max_length=50, choices=location_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    booked_for = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    communication_method = models.CharField(max_length=50, choices=COMMUNICATION_CHOICES, default='')

    def __str__(self):
        return f"Appointment at {self.location} for {self.booked_for} by {self.author.username}"

    def is_upcoming(self):
        """
        Method to check if the appointment is upcoming or not.
        """
        return self.booked_for > timezone.now()
    is_upcoming.boolean = True  # Display as a boolean field in the admin interface

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-booked_for']

class Testimonies(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_full_name(self):
        full_name = self.author.username
        if self.author.first_name and self.author.last_name:
            full_name = self.author.first_name + " " + self.author.last_name
        return full_name

    def __str__(self):
        return f"posted by {self.get_full_name} 👉🏻 {self.content}"