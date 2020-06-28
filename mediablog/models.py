import tempfile

from django.contrib.auth.models import User
from django.contrib.sites import requests
from django.core import files
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

reaction_choices = (("like", "like"), ("heart", "heart"), ("sad", "sad"), ("haha", "haha"), ("angry", "angry"))


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(to="MediaBlog", on_delete=models.CASCADE)
    reaction_type = models.CharField(choices=reaction_choices, max_length=10)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return self.reaction_type


class MediaBlog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40,blank=False)
    link = models.URLField(blank=False)
    description = RichTextField(blank=False)
    thumbnail = models.ImageField(upload_to="mediablog/",blank=False)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    angry = models.ManyToManyField(User, related_name="angry", blank=True)
    love = models.ManyToManyField(User, related_name="love", blank=True)
    sad = models.ManyToManyField(User,related_name='sad',blank=True)
    hahaha = models.ManyToManyField(User,related_name='hahaha',blank=True)
    reactions = models.ManyToManyField(to=Reaction, related_name="reactions", blank=True)
    post_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    def total_reactions(self):
        return self.reactions.count()
    def loved(self):
        return self.objects.filter()
    def liked_count(self):
        return self.likes.count()-1
    def loved_count(self):
        return self.love.count()-1
    def angry_count(self):
        return self.angry.count()-1
    def sad_count(self):
        return self.sad.count()-1
    def hahaha_count(self):
        return self.hahaha.count()-1
    def liked_count_r(self):
        return self.likes.count()
    def loved_count_r(self):
        return self.love.count()
    def angry_count_r(self):
        return self.angry.count()
    def sad_count_r(self):
        return self.sad.count()
    def hahaha_count_r(self):
        return self.hahaha.count()
    def total_react(self):
        return self.hahaha.count()+self.likes.count()+self.love.count()+self.angry.count()+self.sad.count()
    def get_absolute_url(self):
        return reverse("mediadetails",kwargs={"id":self.id})


class Comment(models.Model):
    post = models.ForeignKey(MediaBlog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title,str(self.user.username))

