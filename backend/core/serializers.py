from rest_framework import serializers
from .models import Post # sample model import

# Example serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']