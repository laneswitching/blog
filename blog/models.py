from django.db import models
from django.utils.timezone import now

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=2)
    published_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=now)


    def __str__(self):
        return self.title