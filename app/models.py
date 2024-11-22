from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    ingredients = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='recipe/', blank=True, null=True)
    rating = models.FloatField(default=0)  # Promedio de calificación
    votes = models.IntegerField(default=0)  # Número de votos

    def update_rating(self, new_rating):
        """Actualiza el promedio de calificación."""
        total_score = self.rating * self.votes  # Suma total de calificaciones existentes
        self.votes += 1  # Incrementa el número de votos
        self.rating = (total_score + new_rating) / self.votes  # Calcula el nuevo promedio
        self.save()

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} in {self.recipe.title}"


