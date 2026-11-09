from django.urls import path
from main import api_views

app_name = "api"
urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("reviews/", api_views.review_list, name="review-list"),
    path("reviews/<int:review_id>/", api_views.review_detail, name="review-detail"),
    path("reviews/<int:review_id>/star/", api_views.review_star, name="review-star"),
]