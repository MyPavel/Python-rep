# Generated by Django 4.0.6 on 2022-09-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='postCategory',
        ),
        migrations.AddField(
            model_name='post',
            name='Category',
            field=models.ManyToManyField(related_name='posts', through='news.PostCategory', to='news.category', verbose_name='Категория'),
        ),
    ]