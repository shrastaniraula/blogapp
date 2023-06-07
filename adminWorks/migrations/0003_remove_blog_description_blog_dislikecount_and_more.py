# Generated by Django 4.1.7 on 2023-06-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminWorks', '0002_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='description',
        ),
        migrations.AddField(
            model_name='blog',
            name='dislikeCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='likeCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]