from django.db import models
from django.contrib.auth.models import User
from academy.managers import SliderManager

# Create your models here.
class Rank(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="rank/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Software(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="software/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Category(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="category/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Author(models.Model):
    name = models.CharField(max_length=64)
    bio = models.TextField()
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    social_twitter = models.CharField(max_length=128, blank=True, null=True)
    social_facebook = models.CharField(max_length=128, blank=True, null=True)
    social_instagram = models.CharField(max_length=128, blank=True, null=True)
    social_linkedin = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="course/", null=True, blank=True)
    authors = models.ManyToManyField(Author)
    category = models.ManyToManyField(Category)
    software = models.ManyToManyField(Software)
    rank = models.ManyToManyField(Rank)
    files = models.ManyToManyField('CourseFile', blank=True)
    views = models.ManyToManyField('View', blank=True)
    likes = models.ManyToManyField('Like', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CourseFile(models.Model):
    track_no = models.IntegerField()
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="course_file", null=True, blank=True)
    file = models.CharField(max_length=512)
    duration = models.TimeField()
    views = models.ManyToManyField('View', blank=True)
    likes = models.ManyToManyField('Like', blank=True)

    def __str__(self):
        return '%s - %s' % (self.track_no, self.title)

    class Meta:
        ordering = ('track_no',)

class View(models.Model):
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Slider(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="slider/", null=True, blank=True)
    link = models.URLField()
    link_title = models.CharField(max_length=64, default="Learn more")
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = SliderManager()

    def __str__(self):
        return self.title
