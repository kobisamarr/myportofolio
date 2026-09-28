from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from main.models import Experience, Education, Project, Reviews
from main.forms import ProjectForm, ReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import HttpResponse

import datetime

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Marwa Muhlashon",
        "npm": "2506552714",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I have so much interest in motion graphics and "
            "UI/UX design. I hope I can learn various things "
            "in this new level of education. "
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Marwa Muhlashon",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Marwa Muhlashon",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Marwa Muhlashon",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def create_project(request):
    #jika yang request adalah super user (admin) maka terima
    #jika tidak, maka tolak (403)
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Marwa Muhlashon",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize(
        "json", projects, use_natural_foreign_keys=True
    )
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

def show_reviews(request):
    json_response = get_reviews_json(request)

    reviews = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    reviews = [review.object for review in reviews]

    context = {
        "name": "Marwa Muhlashon",
        "review_list": reviews,
    }

    return render(request, "reviews.html", context)

def create_reviews(request):
    form = ReviewForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Review berhasil ditambahkan! :)")
        return redirect("main:show_reviews")

    context = {
        "name": "Marwa Muhlashon",
        "form": form,
    }

    return render(request, "reviews_form.html", context)

def edit_reviews(request, review_id):
    review = get_object_or_404(Reviews, pk=review_id)
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Review berhasil diperbarui!")
        return redirect("main:show_reviews")

    context = {
        "name": "Marwa Muhlashon",
        "form": form, 
        "review": review, 
    }

    return render(request, "reviews_form.html", context)

def delete_reviews(request, review_id):
    review = get_object_or_404(Reviews, pk=review_id)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review berhasil dihapus!")
        return redirect("main:show_reviews")

def get_reviews_json(request):
    reviews = Reviews.objects.all()
    review_json = serializers.serialize("json", reviews)

    return HttpResponse(
        review_json,
        content_type="application/json"
    )

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Marwa",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Marwa",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response