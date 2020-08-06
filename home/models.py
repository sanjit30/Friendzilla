from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.timezone import now
import datetime
import pytz
import math
# from dateutil.parser import parse
# Create your models here.
class Post(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to='post_images',null = True,default='default.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,default = now)
    created_by = models.ForeignKey(User, related_name='posts',on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')
    def total_likes(self):
        return self.likes.count()
    def total_comments(self):
        return self.comments.count()
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def posted_ago(self):
        # print(type(now))
        # return self.updated_at - now

        time = datetime.datetime.now().replace(tzinfo=None)
        print(time)
        print(self.updated_at)
        original_time = self.updated_at.replace(tzinfo=None)
        diff = time-original_time
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) +  "second ago"

            else:
                return str(seconds) + " seconds ago"



        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank = True,default = now)
    created_by = models.ForeignKey(User,related_name = 'comments',on_delete = models.CASCADE)
    post = models.ForeignKey(Post,related_name = 'comments',on_delete = models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.text)
        return truncated_message.chars(20)
