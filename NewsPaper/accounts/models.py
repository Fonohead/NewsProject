from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.IntegerField(default=0)

    # Подсчёт рейтинга автора.
    def update_rating(self):
        post_score = sum(p.rating for p in self.post_set.all()) * 3
        own_comment_score = sum(c.rating for c in self.user.comments.all())
        post_comment_score = sum(c.rating for p in self.post_set.all() for c in p.comment_set.all())
        self.rating = post_score + own_comment_score + post_comment_score
        self.save()

    def __str__(self):
        return self.user.username




