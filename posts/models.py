from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post Model, Related to 'owner', i.e a User instance.
    Default imahe set so thay we can always reference image.url.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_yyxugh',
        blank=True
    )

    class Meta:
        ordering = ['created_at']

        def __str__(self):
            return f'{self.id} {self.title}'
