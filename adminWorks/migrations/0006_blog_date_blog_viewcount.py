# Generated by Django 4.1.7 on 2023-06-07 15:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminWorks', '0005_alter_blog_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='blog',
            name='viewCount',
            field=models.IntegerField(default=0),
        ),
    ]
