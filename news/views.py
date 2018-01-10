from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer
from .service import search

# Create your views here.
class ArticleList(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        edition = self.request.query_params.get('edition', None)
        language = self.request.query_params.get('language', None)
        country = self.request.query_params.get('country', None)
        query = self.request.query_params.get('query', None)
        return search(edition, language, country, query)