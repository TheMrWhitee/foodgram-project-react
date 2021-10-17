from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name='Единицы измерения')

    def __str__(self):
        return self.name


class Component(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
    amount = models.IntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient.name}, {self.amount}'


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тег')
    color = ColorField(default='#FF0000', verbose_name='Цвет')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name='Тег')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    ingredients = models.ManyToManyField(Component,
                                         related_name='recipes',
                                         verbose_name='Ингредиент')
    name = models.CharField(max_length=200,
                            verbose_name='Название блюда')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Фото')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        validators=(
            MinValueValidator(1, message='Время приготовления должно '
                                         'быть больше 0!'),
        ),
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name


class Favorites(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='favorites',
                              verbose_name='Пользователь')

    recipes = models.ManyToManyField(Recipe,
                                     related_name='favorites',
                                     verbose_name='Рецепт')


class ShoppingCart(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='shopping_cart',
                              verbose_name='Пользователь')

    recipes = models.ManyToManyField(Recipe,
                                     related_name='shopping_cart',
                                     verbose_name='Рецепт')
