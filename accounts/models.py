from django.db import models
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
# Create your models here.
from django.contrib.auth.models import User
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name ='profile',on_delete=models.CASCADE)
    country = models.CharField(max_length=256,blank = True,null = True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True,null = True)
    work = models.CharField(max_length = 512,blank = True,null = True)
    college=  models.CharField(max_length = 512,blank = True,null = True)
    friends = models.ManyToManyField("UserProfile", blank=True)

# def create_profile(sender, instance, created, *args, **kwargs):
#     # ignore if this is an existing User
#     if not created:
#         return
#     UserProfile.objects.create(user=instance)
#
# post_save.connect(create_profile, sender=User)
class FriendRequest(models.Model):
	to_user = models.ForeignKey(User, related_name='to_user',on_delete = models.CASCADE)
	from_user = models.ForeignKey(User, related_name='from_user',on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True) # set when created

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)
