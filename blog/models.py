from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content= models.TextField(blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank = True, null=True)

    def __str__(self):
        return self.title   

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def hide(self):
        self.published_date = None
        self.save()


class NewsData(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __init__(self, title, image, summary, link):
        self.title = title
        self.image = image
        self.summary = summary
        self.link = link

class MoreData(models.Model):
    email = models.CharField(max_length=255, blank=False) # 이메일
    content = models.CharField(max_length=255) #
    published_date = models.CharField(max_length=100, blank = True, null=True)

    # def __str__(self):
    #     return self.email 

    # def __init__(self, email, content, published_date):
    #     self.email = email
    #     self.content = content
    #     self.published_date =timezone.now()

    # def register(self):
    #     self.published_date = timezone.now()
    #     self.save()
