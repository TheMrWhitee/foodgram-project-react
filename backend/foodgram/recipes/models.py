from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

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
    color = ColorField(default='#FF0000')
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
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(1, message='Время приготовления должно '
                                         'быть больше 0!'),
        )
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Favorites(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='favorites')

    recipes = models.ManyToManyField(Recipe)


class ShoppingCart(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='shopping_cart')

    recipes = models.ManyToManyField(Recipe)
