from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Reviews


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class ReviewsSerializer(serializers.ModelSerializer):

    star_count = serializers.SerializerMethodField()

    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Reviews

        fields = [
            "id",
            "name",
            "relationship",
            "review",
            "rating",
            "created_at",
            "star_count",
            "is_starred",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "star_count",
            "is_starred",
        ]

    # Validasi nama dan membersihkan HTML
    def validate_name(self, value):

        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Name cannot be empty."
            )

        return value

    # Validasi relationship
    def validate_relationship(self, value):

        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Relationship cannot be empty."
            )

        return value

    # Validasi isi review
    def validate_review(self, value):

        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Review cannot be empty."
            )

        return value

    # Validasi rating harus 1 sampai 5
    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value

    # Menghitung jumlah star
    def get_star_count(self, obj):

        return obj.starred_by.count()

    # Memeriksa apakah user yang login sudah memberikan star
    def get_is_starred(self, obj):

        request = self.context.get("request")

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(
            pk=request.user.pk
        ).exists()