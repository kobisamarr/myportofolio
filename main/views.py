from django.shortcuts import render

from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "Marwa Muhlashoon",
        "npm": "2506552714",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I have so much interest in motion graphics and "
            "UI/UX design. I hope I can learn various things "
            "in this new level of education. "
        ),
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