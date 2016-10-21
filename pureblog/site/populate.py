# -*- coding:utf-8 -*-
import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pureblog.settings')

import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()

from apps.models import Article, Category, Tag

def populate():
    tags = []
    cat_Python = add_cat('Python')
    tag_django = add_tag('django')
    tags.append(tag_django)
    add_article('标题2', 'p', cat_Python, tags)

def add_article(title, status, cat, tags):
    a = Article.objects.get_or_create(title=title,
            create_time=datetime.datetime.utcnow(),
            last_modified_time=datetime.datetime.utcnow(),
            status=status)[0]
    a.content = '这是测试数据'
    a.abstract = a.content[:64]
    a.category = cat

    for tag in tags:
        a.tags.add(tag)
    a.save()
    return a

def add_cat(name):
    try:
        obj = Category.objects.get(name=name)
    except ObjectDoesNotExist:
        obj = Category(name=name, create_time=datetime.datetime.utcnow())
        obj.save()
    return obj

def add_tag(name):
    try:
        obj = Tag.objects.get(name=name)
    except ObjectDoesNotExist:
        obj = Tag(name=name, create_time=datetime.datetime.utcnow())
        obj.save()
    return obj

if __name__ == '__main__':
    populate()
