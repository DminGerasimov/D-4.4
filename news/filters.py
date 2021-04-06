import django_filters
from news.models import Post


class NewsFilter(django_filters.FilterSet):
    # time_in = 
    class Meta:
        model = Post
        fields = {'author__user':['exact'], 'time_in':['gt']}