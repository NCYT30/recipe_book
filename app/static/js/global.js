const csrfToken = '{{ csrf_token }}';


document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star');
    const ratingDisplay = document.getElementById('rating-value');
    const recipeContainer = document.querySelector('.details-section');
    const recipeId = recipeContainer.getAttribute('data-recipe-id');

    stars.forEach(star => {
        star.addEventListener('mouseover', () => {
            resetStars();
            highlightStars(star);
        });

        star.addEventListener('click', () => {
            const rating = parseInt(star.getAttribute('data-value'));
            ratingDisplay.textContent = rating;
            setSelectedStars(star);
            submitRating(rating);
        });

        star.addEventListener('mouseout', resetStars);
    });

    function resetStars() {
        stars.forEach(star => star.classList.remove('selected'));
    }

    function highlightStars(star) {
        star.classList.add('selected');
        let previous = star.previousElementSibling;
        while (previous) {
            previous.classList.add('selected');
            previous = previous.previousElementSibling;
        }
    }

    function setSelectedStars(star) {
        resetStars();
        highlightStars(star);
    }

    function submitRating(rating) {
        const recipeContainer = document.querySelector('.details-section');
        const recipeId = recipeContainer.getAttribute('data-recipe-id');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Alternative if placed in a hidden input
    
        fetch(`/recipe/${recipeId}/rate/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Ensure this header is passed
            },
            body: JSON.stringify({ rating: rating })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.message) {
                alert(data.message);
                console.log(`Nuevo promedio: ${data.new_average}, Votos: ${data.total_votes}`);
                // Optionally update the UI with new average and votes
            } else if (data.error) {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema al enviar la calificación. Por favor, inténtalo de nuevo.');
        });
    }
    
});


document.addEventListener('DOMContentLoaded', function() {
    const inputBuscar = document.getElementById('input-buscar');
    const contenedorJuegos = document.getElementById('contenedor-recetas');
    if (!inputBuscar || !contenedorJuegos) {
        console.error('Element not found');
        return;
    }

    const juegos = Array.from(contenedorJuegos.children);

    inputBuscar.addEventListener('input', function () {
        const valorBusqueda = inputBuscar.value.trim().toLowerCase();

        juegos.forEach(function (elemento) {
            const nombreReceta = elemento.querySelector('.title').textContent.trim().toLowerCase();
            if (nombreReceta.includes(valorBusqueda) || valorBusqueda === '') {
                elemento.style.display = 'block';
            } else {
                elemento.style.display = 'none';
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const inputBuscar = document.getElementById('input-buscar');
    const contenedorJuegos = document.getElementById('contenedor-recetas-unicas');
    if (!inputBuscar || !contenedorJuegos) {
        console.error('Element not found');
        return;
    }

    const juegos = Array.from(contenedorJuegos.children);

    inputBuscar.addEventListener('input', function () {
        const valorBusqueda = inputBuscar.value.trim().toLowerCase();

        juegos.forEach(function (elemento) {
            const nombreReceta = elemento.querySelector('.title').textContent.trim().toLowerCase();
            if (nombreReceta.includes(valorBusqueda) || valorBusqueda === '') {
                elemento.style.display = 'block';
            } else {
                elemento.style.display = 'none';
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const chatCircle = document.getElementById('chat-circle');
    const chatbox = document.getElementById('chatbox-container');
    const sendBtn = document.getElementById('send-btn');
    const textarea = document.getElementById('chat-textarea');
    const messageBox = document.getElementById('chat-messages');

    chatCircle.addEventListener('click', function () {
        chatbox.style.display = chatbox.style.display === 'none' ? 'flex' : 'none';
    });

    sendBtn.addEventListener('click', function () {
        const userMessage = textarea.value.trim();

        if (userMessage) {
            const userMessageElement = document.createElement('div');
            userMessageElement.textContent = userMessage;
            userMessageElement.style.padding = '5px';
            userMessageElement.style.marginBottom = '5px';
            userMessageElement.style.backgroundColor = '#f1f1f1';
            userMessageElement.style.borderRadius = '5px';
            messageBox.appendChild(userMessageElement);

            // Enviar mensaje al backend
            fetch('/chatbot-response/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Solo si usas CSRF
                },
                body: JSON.stringify({ message: userMessage })
            })
            
                .then(response => response.json())
                .then(data => {
                    const botMessageElement = document.createElement('div');
                    botMessageElement.textContent = data.reply;
                    botMessageElement.style.padding = '5px';
                    botMessageElement.style.marginBottom = '5px';
                    botMessageElement.style.backgroundColor = '#e0f7fa';
                    botMessageElement.style.borderRadius = '5px';
                    messageBox.appendChild(botMessageElement);

                    messageBox.scrollTop = messageBox.scrollHeight;
                })
                .catch(error => {
                    console.error('Error:', error);
                });

            textarea.value = '';
        }
    });
});

// Función para obtener el token CSRF (necesaria si no usas @csrf_exempt)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
