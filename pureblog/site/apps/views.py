import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView, SingleObjectMixin

from .models import Article, Category, Tag


class IndexView(ListView, MultipleObjectMixin):
    template_name = 'apps/index.html'
    context_object_name = 'article_list'
    paginate_by = 2

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        return article_list

class ArticleDetailView(DetailView, SingleObjectMixin):
    template_name = 'apps/detail.html'
    context_object_name = 'article'
    queryset = Article.objects.all()
    pk_url_kwarg = 'article_id'

    def get(self, request, *args, **kwargs):
        last_visit = request.session.get('last_visit')
        reset_last_visit_time = False

        if last_visit:
            last_visit_time = datetime.datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

            if (datetime.datetime.utcnow() - last_visit_time).seconds > 0:
                obj = super(ArticleDetailView, self).get_object() 
                obj.views = obj.views + 1 
                obj.save()
                reset_last_visit_time = True
        else:
            reset_last_visit_time = True

        if reset_last_visit_time:
            request.session['last_visit'] = str(datetime.datetime.utcnow())

        return super(ArticleDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        object = super(ArticleDetailView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        object = super(ArticleDetailView, self).get_object()
        context['tags'] = object.tags.all()
        return context

class ArchiveView(ListView, MultipleObjectMixin):
    template_name = 'apps/full-width.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        return article_list

class CategoryView(ListView, MultipleObjectMixin):
    template_name = 'apps/full-width.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        cat_query = Category.objects.get(name=self.kwargs['category'])
        article_list = cat_query.article_set.filter(status='p')
        return article_list

class TagView(ListView):
    template_name = 'apps/full-width.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        tag_query = Tag.objects.get(name=self.kwargs['tag'])
        article_list = tag_query.article_set.filter(status='p')
        return article_list

class DateView(ListView):
    template_name = 'apps/full-width.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        start_date = datetime.date(int(year), int(month), 1)
        end_date = datetime.date(int(year), int(month), 31)
        article_list = Article.objects.filter(create_time__range=(start_date, end_date))

        return article_list


