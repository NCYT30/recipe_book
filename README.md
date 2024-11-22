# Recipe App with AI Chatbot

Esta aplicación web permite a los usuarios buscar recetas, crear sus propias recetas, calificarlas y ver las mejores recetas basadas en las calificaciones de otros usuarios. Además, cuenta con un **chatbot** con **inteligencia artificial** que responde preguntas sobre recetas y ayuda a encontrar recetas similares.

## Características

- **Búsqueda de recetas**: Los usuarios pueden buscar recetas por título o categoría.
- **Creación de recetas**: Los usuarios pueden crear sus propias recetas, agregar ingredientes, instrucciones y subir una imagen.
- **Sistema de calificación**: Los usuarios pueden calificar las recetas con un máximo de 5 estrellas.
- **Mejores recetas**: Las recetas con las calificaciones más altas se muestran en un módulo de "Mejores recetas".
- **Chatbot con inteligencia artificial**: Un chatbot que responde preguntas sobre recetas y puede recomendar recetas basadas en la similitud semántica de la consulta.

## Tecnologías utilizadas

El proyecto está basado en las siguientes tecnologías:

- **Django**: Framework web para construir la aplicación.
- **MySql**: Base de datos para almacenar las recetas y datos del usuario.
- **Python**: Lenguaje de programación principal.
- **Transformers (Hugging Face)**: Para la implementación de un modelo de lenguaje que ayuda al chatbot a generar respuestas.
- **SpaCy**: Procesamiento de lenguaje natural para mejorar las interacciones con el chatbot.
- **FuzzyWuzzy**: Para la comparación de similitudes entre títulos de recetas.
- **Scikit-learn**: Para el cálculo de similitudes entre recetas mediante embeddings.

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto localmente:

### 1. Clona el repositorio

```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
