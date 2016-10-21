# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    title = models.CharField('标题', max_length=64, unique=True)
    content = models.TextField('正文')
    create_time = models.DateTimeField('创建时间')
    last_modified_time = models.DateTimeField('修改时间')
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=64, blank=True, null=True, help_text='可选，如若为空将摘取正文的前64个字符')
    views = models.PositiveIntegerField('浏览次数', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)

    category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-last_modified_time']

class Category(models.Model):
    name = models.CharField('类名', max_length=20, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('标签名', max_length=20, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.name

class Visitor(models.Model):
    visitor_ip = models.CharField('游客ip', max_length=64, unique=True)
