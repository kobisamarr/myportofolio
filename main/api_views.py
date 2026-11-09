from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Project, Reviews
from main.permissions import IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import ProjectSerializer, ReviewsSerializer
from django.db.models import Q


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)

@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def review_list(request):

    if request.method == "GET":

        reviews = Reviews.objects.prefetch_related(
            "starred_by"
        ).order_by("-created_at")

        search = request.query_params.get(
            "search", ""
        ).strip()

        if search:
            reviews = reviews.filter(
                Q(name__icontains=search) |
                Q(relationship__icontains=search) |
                Q(review__icontains=search)
            )

        serializer = ReviewsSerializer(
            reviews,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    serializer = ReviewsSerializer(
        data=request.data,
        context={"request": request}
    )

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def review_detail(request, review_id):

    review = get_object_or_404(
        Reviews.objects.prefetch_related("starred_by"),
        pk=review_id
    )

    if request.method == "GET":

        serializer = ReviewsSerializer(
            review,
            context={"request": request}
        )

        return Response(serializer.data)

    if request.method == "DELETE":

        review.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    serializer = ReviewsSerializer(
        review,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request}
    )

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def review_star(request, review_id):

    review = get_object_or_404(
        Reviews,
        pk=review_id
    )

    if review.starred_by.filter(
        pk=request.user.pk
    ).exists():

        review.starred_by.remove(request.user)

    else:

        review.starred_by.add(request.user)

    serializer = ReviewsSerializer(
        review,
        context={"request": request}
    )

    return Response(serializer.data)