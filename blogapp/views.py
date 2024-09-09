from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from accounts.decorators import staff_required
from .models import *
from django.http import HttpResponseNotFound
from django.conf import settings
import random
import string
import os
from django.http import HttpResponse
from accounts.models import Student, User
from academy.models import Course
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render




# ########################################################
# News & Events
# ########################################################
def home_view(request):
    search_query = request.GET.get("keyword", "")
    print(search_query)
    blogs = Blogs.objects.filter(Q(title__icontains=search_query) | Q(posted_as__icontains=search_query)).order_by('-updated_date')
    num_results = blogs.count()
    # Fetch testimonies
    testimonies = Testimonies.objects.order_by('-created_at')
    # Pagination for blogs
    blog_page = request.GET.get("blog_page", 1)
    blog_results_per_page = 8
    blog_paginator = Paginator(blogs, blog_results_per_page)
    try:
        blogs = blog_paginator.page(blog_page)
    except PageNotAnInteger:
        blogs = blog_paginator.page(1)
    except EmptyPage:
        blogs = blog_paginator.page(blog_paginator.num_pages)

    # Pagination for testimonies
    testimony_page = request.GET.get("testimony_page", 1)
    testimony_results_per_page = 8
    testimony_paginator = Paginator(testimonies, testimony_results_per_page)
    try:
        testimonies = testimony_paginator.page(testimony_page)
    except PageNotAnInteger:
        testimonies = testimony_paginator.page(1)
    except EmptyPage:
        testimonies = testimony_paginator.page(testimony_paginator.num_pages)

    items = Blogs.objects.all().order_by('-updated_date')
    context = {
        'title': "Checking>>> | Jay TechnLogic",
        'items': items,
        "blogs": blogs,
        "testimonies": testimonies,
        "search_query": search_query,
        "blog_paginator": blog_paginator,
        "testimony_paginator": testimony_paginator,
        "num_results": num_results,

    }
    return render(request, 'app/index.html', context)


@login_required
def post_add(request):
    if request.method == 'POST':
        form = BlogsForm(request.POST)
        title = request.POST.get('title')
        if form.is_valid():
            form.save()

            messages.success(request, (title + ' has been uploaded.'))
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = BlogsForm()
    return render(request, 'app/post_add.html', {
        'title': 'Add Post | Jay TechnLogic',
        'form': form,
    })


@login_required
@staff_required
def edit_post(request, pk):
    instance = get_object_or_404(Blogs, pk=pk)
    if request.method == 'POST':
        form = BlogsForm(request.POST, instance=instance)
        title = request.POST.get('title')
        if form.is_valid():
            form.save()

            messages.success(request, (title + ' has been updated.'))
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = BlogsForm(instance=instance)
    return render(request, 'app/post_add.html', {
        'title': 'Edit Post | Jay TechnLogic',
        'form': form,
    })


@login_required
@staff_required
def delete_post(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, (title + ' has been deleted.'))
    return redirect('home')

def detail(request, slug):
    blog = get_object_or_404(Blogs, slug=slug)
    comments = Comment.objects.filter(blog=blog)
    context = {"blog": blog,"comments": comments}
    return render(request, "blogapp/detail.html", context)



def terms(request):
    if request.method == 'POST':
        # Process the form submission here
        # ...
        return render(request, 'blogapp/maintain.html')
    else:
        return render(request, 'blogapp/terms.html')


def privacy(request):
    if request.method == 'POST':
        # Process the form submission here
        # ...
        return render(request, 'blogapp/maintain.html')
    else:
        return render(request, 'blogapp/privacy.html')


def maintain(request):
    if request.method == 'POST':
        # Process the form submission here
        # ...
        return render(request, 'blogapp/maintain.html')
    else:
        return render(request, 'blogapp/maintain.html')


def navslide(request):
    search_query = request.GET.get("keyword", "")
    print(search_query)

    blogs = Blogs.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    blog_filters = {
        "webs": Blogs.objects.filter(is_web=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "school": Blogs.objects.filter(is_school=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "auto": Blogs.objects.filter(is_auto=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "shop": Blogs.objects.filter(is_shopping=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "social": Blogs.objects.filter(is_social=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "block": Blogs.objects.filter(is_blockchain=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "fashion": Blogs.objects.filter(is_fashion=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "real": Blogs.objects.filter(is_real_estate=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "hotel": Blogs.objects.filter(is_hotel=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "others": Blogs.objects.filter(is_others=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "appdev": Blogs.objects.filter(is_appdev=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "mobile": Blogs.objects.filter(is_mobile=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "cross": Blogs.objects.filter(is_cross=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "mark": Blogs.objects.filter(is_markerting=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "seo": Blogs.objects.filter(is_SEO=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "smm": Blogs.objects.filter(is_SMM=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "emailing": Blogs.objects.filter(is_Emailing=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "pcc": Blogs.objects.filter(is_PPC=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "cont": Blogs.objects.filter(is_content=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "others_mark": Blogs.objects.filter(is_others_markerting=True, status=Blog.Status.PUBLISHED).order_by(
            '-created'),
        "prod": Blogs.objects.filter(is_productcat=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "erp": Blogs.objects.filter(is_ERP=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "crm": Blogs.objects.filter(is_CRM=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "cms": Blogs.objects.filter(is_CMS=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "cloud": Blogs.objects.filter(is_CloudB=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "bi": Blogs.objects.filter(is_BI=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "cysec": Blogs.objects.filter(is_cyber_security=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "tips": Blogs.objects.filter(is_tips=True, status=Blog.Status.PUBLISHED).order_by('-created'),
        "guide": Blogs.objects.filter(is_guide=True, status=Blog.Status.PUBLISHED).order_by('-created'),
    }

    num_results = blogs.count()

    blog_page = request.GET.get("blog_page", 1)
    blog_results_per_page = 4
    blog_paginator = Paginator(blogs, blog_results_per_page)
    try:
        blogs = blog_paginator.page(blog_page)
    except PageNotAnInteger:
        blogs = blog_paginator.page(1)
    except EmptyPage:
        blogs = blog_paginator.page(blog_paginator.num_pages)

    context = {
        "blogs": blogs,
        "search_query": search_query,
        "blog_paginator": blog_paginator,
        "num_results": num_results,
        "blog_filters": blog_filters,  # Adding blog filters to the context

    }

    return render(request, "blogapp/navslide.html", context)


def testimony_list(request):
    testimonies = Testimonies.objects.order_by('-created_at').all()
    post_paginator = Paginator(testimonies, 6)
    post_page_number = request.GET.get('post_page')
    try:
        testimonies = post_paginator.page(post_page_number)
    except PageNotAnInteger:
        testimonies = post_paginator.page(1)
    except EmptyPage:
        testimonies = post_paginator.page(post_paginator.num_pages)

    context = {
        'testimonies': testimonies
    }
    return render(request, 'blogapp/index.html', context)


@login_required
def create_testimony(request):
    search_query = request.GET.get("keyword", "")
    print(search_query)

    # Fetch blogs based on search query
    blogs = Blogs.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    num_results = blogs.count()

    # Fetch testimonies
    testimonies = Testimonies.objects.order_by('-created_at')

    # Pagination for blogs
    blog_page = request.GET.get("blog_page", 1)
    blog_results_per_page = 4
    blog_paginator = Paginator(blogs, blog_results_per_page)
    try:
        blogs = blog_paginator.page(blog_page)
    except PageNotAnInteger:
        blogs = blog_paginator.page(1)
    except EmptyPage:
        blogs = blog_paginator.page(blog_paginator.num_pages)

    # Pagination for testimonies
    testimony_page = request.GET.get("testimony_page", 1)
    testimony_results_per_page = 8
    testimony_paginator = Paginator(testimonies, testimony_results_per_page)
    try:
        testimonies = testimony_paginator.page(testimony_page)
    except PageNotAnInteger:
        testimonies = testimony_paginator.page(1)
    except EmptyPage:
        testimonies = testimony_paginator.page(testimony_paginator.num_pages)

    if request.method == 'POST':
        form = TestimonyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Successful')
            return redirect('index')
    else:
        form = TestimonyForm()
    context = {
        "blogs": blogs,
        "testimonies": testimonies,
        "search_query": search_query,
        "blog_paginator": blog_paginator,
        "testimony_paginator": testimony_paginator,
        "num_results": num_results,
        'form': form
    }
    return render(request, "blogapp/index.html", context)


def generate_random_code():
    return ''.join(random.choices(string.digits, k=6))

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'blogapp/appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        # Check if the user already has an appointment booked at the same time
        if Appointment.objects.filter(booked_for=form.cleaned_data['booked_for'], is_booked=True).exists():
            messages.error(self.request, 'This appointment slot is already booked. Please select a different date.')
            return self.render_to_response(self.get_context_data(form=form))

        # Check if the user has any existing appointments that are not attended to
        if Appointment.objects.filter(author=self.request.user, is_booked=False).exists():
            messages.error(self.request, 'You already have an appointment pending.')
            return redirect('appointment_list')

        # Proceed with booking if no conflicting appointments exist
        form.instance.author = self.request.user
        return super().form_valid(form)


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'blogapp/appointment_form.html'
    success_url = reverse_lazy('appointment_list')


def download_pdf(request):
    # Path to the PDF file
    pdf_file_path = os.path.join(settings.BASE_DIR, 'media', 'file.pdf')

    # Check if the file exists
    if not os.path.exists(pdf_file_path):
        return HttpResponseNotFound('The requested file does not exist.')

    try:
        # Open the PDF file for reading in binary mode
        with open(pdf_file_path, 'rb') as pdf_file:
            # Read the file content into a variable
            pdf_content = pdf_file.read()

        # Return the PDF file as a FileResponse
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="EASY_JAY_CONTRACT.pdf"'
        return response
    except Exception as e:
        # Handle any exceptions
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'blogapp/appointment_list.html'  # Define the template
    context_object_name = 'appointments'  # Define the context object name

    def get_queryset(self):
        # Filter appointments to only include appointments associated with the current user
        return Appointment.objects.filter(author=self.request.user)


class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment_list')

def hilltop_statistics_view(request):
    # Count the total number of students
    total_students = Student.objects.count()
    total_teacher = Course.objects.count()  # count as number of Sujects
    total_user = User.objects.count()  # count as number of Sujects

    # Add 200 to the total number of students
    total_students += 200
    total_teacher += 40
    total_user += 300

    context = {
        'total_students': total_students,
        'total_teacher': total_teacher,
        'total_user': total_user,
    }
    return render(request, 'app/dashboard.html', context)



def mailing_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Send email
        subject = 'Client Review Form'
        email_message = f'Name: {name}\nEmail: {email}\nphone: {phone}\nMessage: {message}'
        sender = 'From the Contact Form'  # Replace with your email address
        recipients = ['Easy-Jay Technology UPDATE OFFICERS']  # Replace with recipient email addresses

        send_mail(subject, email_message, sender, recipients)

        messages.success(request, 'Form submitted successfully!')
        return redirect('home')

    # Render the contact form
    return render(request, 'app/contact.html')
