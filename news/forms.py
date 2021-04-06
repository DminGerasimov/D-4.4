from django.forms import ModelForm
from .models import Post

class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type_news_article', 'chapter', 'text', 'category']