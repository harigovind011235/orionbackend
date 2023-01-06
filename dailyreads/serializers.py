
from rest_framework import serializers
from .models import Blogs,News


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__'



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
