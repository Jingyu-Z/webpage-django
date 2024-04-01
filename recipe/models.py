from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)  # Path relative to MEDIA_ROOT
    categories = models.ManyToManyField(Category, related_name='recipes', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]  # Return the first 20 characters of the comment

class PageComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]



