from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Component(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.ingredient.name}, {self.amount}'


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    ingredients = models.ManyToManyField(Component)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.name
