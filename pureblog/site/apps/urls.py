from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static 
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^archive/$', views.ArchiveView.as_view(), name='archive'),
    url(r'^article/page(?P<page>\d+)/$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)/$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^archive/category/(?P<category>\w+)/$', views.CategoryView.as_view(), name='catview'),
    url(r'^archive/tag/(?P<tag>\w+)/$', views.TagView.as_view(), name='tagview'),
    url(r'^archive/date/(?P<year>\w+)/(?P<month>\w+)/$', views.DateView.as_view(), name='dateview'),
    url(r'^about/$', TemplateView.as_view(template_name='apps/about.html'), name='about'),
]


if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
