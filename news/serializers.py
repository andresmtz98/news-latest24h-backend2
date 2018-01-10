from .models import Article
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'description', 'source', 'url', 
        'urlImage', 'publishedAt')