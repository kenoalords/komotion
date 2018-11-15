from django.contrib import admin
from academy.models import Category, Author, Course, CourseFile, Slider, Software, Rank, Subscription, Payment
# Register your models here.
admin.site.register(Slider)
admin.site.register(Author)
admin.site.register(Course)
admin.site.register(CourseFile)
admin.site.register(Software)
admin.site.register(Category)
admin.site.register(Rank)
admin.site.register(Subscription)
admin.site.register(Payment)
