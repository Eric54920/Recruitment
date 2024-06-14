from . import models
import django_filters

class NewsFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = models.News
        fields = ['id', 'user', 'pub_date']

class ArticleFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(lookup_expr='exact')
    tag = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = models.Article
        fields = ['id', 'user', 'pub_date', 'tag']

class ResumeFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(lookup_expr='exact')
    class Meta:
        model = models.Resume
        fields = ['id', 'user']

class ChatRecordFilter(django_filters.FilterSet):
    send = django_filters.NumberFilter(lookup_expr='exact')
    receive = django_filters.NumberFilter(lookup_expr='exact')
    class Meta:
        model = models.ChatRecord
        fields = ['send', 'receive']