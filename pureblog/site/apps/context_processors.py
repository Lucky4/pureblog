# -*- coding:utf-8 -*-
from django.db.models import Count
from .models import Article, Category, Tag


def sidebar(request):
    # 取出构造侧栏时需要用到的信息.
    recent_posts = Article.objects.filter(status__exact='p').order_by('create_time')[:3]
    unregular_dates = Article.objects.values_list('create_time').order_by('-create_time')
    category_list = Category.objects.filter(article__status='p').annotate(number_of_articles=Count('article'))
    tag_list = Tag.objects.filter(article__status='p').annotate(number_of_articles=Count('article'))

    # 初始化构造归档时用到的数据.
    dates = []
    temp_dates = []
    month_count = 1
    piece = {}
    dates_tuple = [(date[0].year, date[0].month) for date in unregular_dates]

    """
    如果一个元组信息不再temp_dates中，
    那么就将其相关信息插入导返回结果中，
    并且将记录每月博客数量变量month_count设置为1
    """
    for date in dates_tuple:
        month_count += 1

        if date not in temp_dates:
            piece['year'] = date[0]
            piece['month'] = date[1]
            piece['count'] = month_count

            temp_dates.append(date)
            dates.append(piece) 
            month_count = 1

    return {
        'recent_posts': recent_posts,
        'dates': dates,
        'category_list': category_list,
        'tag_list': tag_list
    }
