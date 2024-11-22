from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
from django.conf import settings
import os
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import logging
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import spacy
from django.views.decorators.csrf import csrf_exempt
from spacy.lang.es.stop_words import STOP_WORDS
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz  # Si prefieres usar fuzzywuzzy para la similitud






def home(request):
    recipe = Recipe.objects.all()
    return render(request, 'home.html', {'recipe': recipe})


def recipe_page(request):
    categor = Category.objects.all()
    return render(request, 'recipe.html', {'categor': categor})


def rate_recipe(request, id):
    if request.method == 'POST':
        try:
            print(f"Incoming POST request for recipe ID: {id}")
            recipe = get_object_or_404(Recipe, id=id)
            data = json.loads(request.body)  # Leer datos JSON enviados
            print(f"Received data: {data}")

            new_rating = int(data.get('rating', 0))
            print(f"New rating value: {new_rating}")

            if not (1 <= new_rating <= 5):  # Validar que la calificación esté entre 1 y 5
                return JsonResponse({'error': 'La calificación debe estar entre 1 y 5.'}, status=400)

            recipe.update_rating(new_rating)  # Actualizar la calificación
            print("Rating updated successfully")

            return JsonResponse({
                'message': 'Calificación registrada con éxito.',
                'new_average': recipe.rating,
                'total_votes': recipe.votes,
            })

        except Exception as e:
            print(f"Error occurred: {e}")  # This will print the actual error to the server console
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():

            form.instance.rating = 0
            form.instance.votes = 0
            
            image_file = request.FILES['imagen'] 
            file_name = os.path.join('recipe', image_file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            form.instance.imagen = file_name

            form.save()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'home.html', {'form': form})


def category(request):
    return render(request, 'recipe.html')


def saurce(request, id):
    try:
        saurce = Recipe.objects.get(id=id)

        data = {
            'id': saurce.id,  # Asegúrate de pasar el ID al contexto
            'title': saurce.title,
            'description': saurce.description,
            'instructions': saurce.instructions,
            'ingredients': saurce.ingredients,
            'imagen': saurce.imagen,
            'imagen': saurce.imagen,
            'category_id': saurce.category.id,
            'category_name': saurce.category.name,
            'rating': getattr(saurce, 'rating', 0),
            'votes': getattr(saurce, 'votes', 0),
        }

        return render(request, 'saucer.html', {'data': data, 'range': range(1, 6)})
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)
    except Exception as e:
        print('Error in get_recipe_id', e)
        return JsonResponse({'error': 'Error internal server'}, status=500)


def top(request):
    # Filtrar todas las recetas con una puntuacion mayor a 3
    recipes = Recipe.objects.filter(rating__gt = 3)

    # Pasa las recetas filtradas al template 'top.html'
    return render(request, 'top.html', {'recipes': recipes})


def base(request):
    recipe = Recipe.objects.get(id=1)
    # Split ingredients and instructions in the view
    recipe_ingredients = recipe.ingredients.split(',')
    recipe_instructions = recipe.instructions.split('.')
    return render(request, 'base.html', {'recipe_ingredients': recipe_ingredients, 'recipe_instructions': recipe_instructions})


# Cargar modelo de embeddings
embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Generar embeddings para las recetas
def generate_recipe_embeddings():
    recipes = Recipe.objects.all()
    embeddings = []
    for recipe in recipes:
        text = f"{recipe.title} {recipe.description}"
        embedding = embedding_model.encode(text)
        embeddings.append((recipe.id, embedding))
    return embeddings

# Buscar receta más similar
def find_most_similar_recipe(query):
    recipes = Recipe.objects.all()
    most_similar = None
    highest_similarity = 0

    for recipe in recipes:
        similarity = fuzz.ratio(query.lower(), recipe.title.lower())
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar = recipe

    return most_similar, highest_similarity

logger = logging.getLogger(__name__)
@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip().lower()

            if not user_message:
                return JsonResponse({'reply': 'Por favor, envía un mensaje válido.'}, status=400)

            if user_message.startswith("quiero más información sobre"):
                recipe_title = (
                    user_message.replace("quiero más información sobre", "").strip(" '").lower()
                )
                recipe = Recipe.objects.filter(title__iexact=recipe_title).first()

                if recipe:
                    # Formatear ingredientes en lista
                    ingredients = "\n".join(
                        f"- {line.strip()}" for line in recipe.ingredients.split("\n") if line.strip()
                    )
                    
                    # Formatear instrucciones en pasos
                    steps = recipe.instructions.split("PASO")
                    formatted_steps = "\n".join(
                        f"**PASO {i+1}:** {step.strip()}" for i, step in enumerate(steps) if step.strip()
                    )

                    # Generar respuesta formateada
                    response = (
                        f"**{recipe.title}**\n\n"
                        f"**Descripción:**\n{recipe.description}\n\n"
                        f"**Ingredientes:**\n{ingredients}\n\n"
                        f"**Instrucciones:**\n{formatted_steps}\n\n"
                        "¡Espero que disfrutes cocinando esta receta! ¿Necesitas ayuda con algo más?"
                    )
                else:
                    response = (
                        f"Lo siento, no encontré información sobre '{recipe_title}'. "
                        "Por favor, verifica el nombre y vuelve a intentarlo."
                    )

            else:
                # Similaridad semántica
                most_similar_recipe, similarity = find_most_similar_recipe(user_message)

                if most_similar_recipe:
                    response = (
                        f"Encontré una receta que coincide con tu búsqueda:\n\n"
                        f"**{most_similar_recipe.title}** (Similitud: {similarity:.2f}%)\n"
                        f"_{most_similar_recipe.description}_\n\n"
                        "¿Te gustaría más información sobre esta receta? Si es así, escribe: "
                        f"'quiero más información sobre {most_similar_recipe.title}'."
                    )
                else:
                    response = (
                        "No encontré recetas similares a tu consulta. Intenta buscar algo diferente o más específico."
                    )

            return JsonResponse({'reply': response})

        except Exception as e:
            logger.error(f"Error procesando la solicitud: {str(e)}")
            return JsonResponse({'reply': 'Ocurrió un error al procesar tu solicitud.'}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
