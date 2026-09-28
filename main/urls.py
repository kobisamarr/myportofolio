from django.urls import path

from main.views import (
    show_main, show_experience, show_education, 
    show_projects, create_project, get_projects_json, delete_project, toggle_star,
    show_reviews, create_reviews, edit_reviews, delete_reviews, get_reviews_json,
    register, login_user, logout_user
    )

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_experience, name="show_experience"),

    path("education/", show_education, name="show_education"),

    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project,name="delete_project"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),

    path("reviews/", show_reviews, name="show_reviews"),
    path("reviews/add/", create_reviews, name="create_reviews"),
    path("reviews/<int:review_id>/edit/", edit_reviews, name="edit_reviews"),
    path("reviews/<int:review_id>/delete/", delete_reviews, name="delete_reviews"),
    path("api/reviews/", get_reviews_json, name="get_reviews_json"),

    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]