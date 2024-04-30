from django.shortcuts import render
from .models import Question


def trivia_view(request):
    if request.method == 'POST':
        # Procesar la respuesta y realizar cualquier acción necesaria aquí
        # Por ejemplo, guardar la respuesta del usuario, verificar si es correcta, etc.
        pass

    # Obtener la pregunta actual
    current_question_id = request.session.get('current_question_id', 1)
    current_question = Question.objects.get(id=current_question_id)

    # Obtener la siguiente pregunta
    next_question_id = current_question_id + 1
    next_question = Question.objects.filter(id=next_question_id).first()

    # Actualizar el ID de la pregunta actual en la sesión
    request.session['current_question_id'] = next_question_id

    return render(request, 'trivia/trivia_game.html', {'question': current_question})


def check_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option_id = request.POST.get('option')
        
        try:
            question = Question.objects.get(pk=question_id)
            correct_option = question.option_set.get(is_correct=True)
            
            if selected_option_id == str(correct_option.id):
                message = "¡Correcto!"
            else:
                message = f"Incorrecto. La respuesta correcta era: {correct_option.text}"
        except Question.DoesNotExist:
            message = "La pregunta no existe."
        except correct_option.DoesNotExist:
            message = "La opción correcta para esta pregunta no existe."
        
        return render(request, 'trivia/answer.html', {'message': message})
    