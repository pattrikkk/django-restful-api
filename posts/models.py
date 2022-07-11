from django.db import models

class Post(models.Model):
    postid = models.IntegerField(primary_key=True)
    userid = models.IntegerField()
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.postid) + " " + self.title