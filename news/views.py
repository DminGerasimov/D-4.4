from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from .filters import NewsFilter
from .forms import NewsForm

class NewsList(ListView):
    model = Post
    template_name = 'news/newslist.html'
    context_object_name = 'newslist'
    ordering = ['-time_in'] # выводим первыми самые свежие новости
    paginate_by = 2


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/newsdetail.html'
    context_object_name = 'newsdetail'  


class SearchNews(ListView):
    model = Post
    template_name = 'news/searchnews.html'
    context_object_name = 'searchnews'

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context["filter"] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context


class NewsAdd(CreateView):
    template_name = 'news/addnews.html'
    form_class = NewsForm


class NewsEdit(UpdateView):
    template_name = 'news/addnews.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    model = Post
    context_object_name = 'newsdetail'  
    template_name = 'news/deletenews.html'
    queryset = Post.objects.all()
    success_url = '/news/'