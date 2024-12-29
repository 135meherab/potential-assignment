from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from forum.models import Forum, ForumComment, ForumImage, Tag
from options.models import City, Province


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "tag_name",
        )


class TagCreateSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "tag_name_en", "tag_name_ko")


class ForumCommentsSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ForumComment
        fields = (
            "id",
            "user",
            "content",
            "image",
            "created_at",
            "replies",
            "parent_comment",
        )
        # write_only_fields = ("article", "parent_comment",)
        extra_kwargs = {
            # "article": {"write_only": True},
            "parent_comment": {"write_only": True},
            # "user": {"read_only": True},
        }

    def get_replies(self, obj):
        # Get all replies for the current comment
        replies = obj.replies.all()
        return ForumCommentsSerializer(
            replies, many=True, context={"request": self.context.get("request")}
        ).data

    def get_user(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.user.id,
            "full_name": obj.user.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.user.user_information.profile_picture.url
                )
                if obj.user.user_information.profile_picture
                else None
            ),
        }

    def validate_parent_comment(self, value):
        if value:
            forum_slug = self.context.get("view").kwargs.get("slug")
            if value.forum.slug != forum_slug:
                raise serializers.ValidationError("Must belong to the same forum.")

        return value


class ForumImageSerializer(ModelSerializer):
    class Meta:
        model = ForumImage
        fields = ("image",)


class ForumListSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Forum
        fields = [
            "id",
            "slug",
            "title",
            "content",
            "tags",
            "total_like",
            "total_comment",
            "created_at",
            "updated_at",
            "user",
            "is_liked",
        ]

    def get_is_liked(self, obj):
        user_likes = self.context.get("user_likes", set())
        return obj.id in user_likes

    def get_user(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.user.id,
            "full_name": obj.user.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.user.user_information.profile_picture.url
                )
                if obj.user.user_information.profile_picture
                else None
            ),
        }


class ForumDetailSerializer(ModelSerializer):
    forum_images = ForumImageSerializer(many=True, read_only=True, source="images")
    tags = TagSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    forum_comments = ForumCommentsSerializer(many=True, read_only=True)

    tag_id = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, required=True
    )
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Forum
        fields = (
            "id",
            "slug",
            "title",
            "content",
            "tags",
            "tag_id",
            "forum_images",
            "total_like",
            "total_comment",
            "created_at",
            "updated_at",
            "images",
            "user",
            "forum_comments",
        )
        read_only_fields = ("user", "slug", "total_like", "total_comment")

    def get_user(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.user.id,
            "full_name": obj.user.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.user.user_information.profile_picture.url
                )
                if obj.user.user_information.profile_picture
                else None
            ),
        }

    @staticmethod
    def validate_tag_id(obj):
        if obj is None or len(obj) == 0:
            raise serializers.ValidationError("This field is required.")
        return obj

    @transaction.atomic
    def create(self, validated_data):
        images = validated_data.pop("images", None)
        tags_ids = validated_data.pop("tag_id", [])

        forum = Forum.objects.create(**validated_data)
        images_obj = [
            ForumImage(forum=forum, image=image_data) for image_data in images
        ]
        ForumImage.objects.bulk_create(images_obj)

        forum.tags.set(tags_ids)  # Use set() to assign the tags
        return forum

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags.set(tags)  # Use set() to update the tags
        return instance
