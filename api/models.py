# models.py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, default='General')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles", null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    comments = models.ManyToManyField('Comment', related_name='article_comments', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.id}/'
    
    def get_author_data(self):
        """Encapsulate author data fetching in a separate method."""
        if self.author:
            return {
                'id': self.author.id,
                'username': self.author.username,
                'email': self.author.email
            }
        return None
    
    def get_data(self):
        """Encapsulate article data retrieval into a dictionary format."""
        return {
            'title': self.title,
            'body': self.body,
            'author': self.get_author_data(),
            'category': self.category.name if self.category else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'comments': [comment.to_dict() for comment in self.comments.all()],
            'images': [image.to_dict() for image in self.images.all()],
            'id': self.id
        }

class Image(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.article.title}"

    def to_dict(self):
        """Encapsulate image data retrieval in a dictionary format."""
        return {
            'article': self.article.id,
            'image': self.image.url if self.image else None
        }

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='article_comments', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Comment by {self.author.username if self.author else 'Anonymous'} on {self.article.title}"

    def to_dict(self):
        """Encapsulate comment data retrieval in a dictionary format."""
        return {
            'id': self.id,
            'author': self.author.username if self.author else 'Anonymous',
            'body': self.body,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }