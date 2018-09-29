# Generated by Django 2.0.2 on 2018-09-03 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0004_auto_20180903_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='files',
            field=models.ManyToManyField(blank=True, to='academy.CourseFile'),
        ),
        migrations.AlterField(
            model_name='course',
            name='likes',
            field=models.ManyToManyField(blank=True, to='academy.Like'),
        ),
        migrations.AlterField(
            model_name='course',
            name='views',
            field=models.ManyToManyField(blank=True, to='academy.View'),
        ),
    ]
