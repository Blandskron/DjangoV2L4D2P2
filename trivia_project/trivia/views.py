from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .models import Question

def trivia_view(request):
    if request.method == 'POST':
        # Procesar la respuesta del usuario
        question_id = request.POST.get('question_id')
        selected_option_id = request.POST.get('answer')
        
        try:
            question = Question.objects.get(pk=question_id)
            correct_option = question.option_set.get(is_correct=True)
            
            if selected_option_id == str(correct_option.id):
                message = "¡Correcto!"
                # Obtener la siguiente pregunta
                next_question = Question.objects.filter(id__gt=question_id).order_by('id').first()
                if next_question:
                    # Actualizar el current_question_id en la sesión
                    request.session['current_question_id'] = next_question.id
                else:
                    # Si no hay más preguntas, eliminar el current_question_id de la sesión
                    del request.session['current_question_id']
                    return render(request, 'trivia/trivia_game.html', {'message': "¡Felicidades! Has completado todas las preguntas. ¿Deseas volver a comenzar?"})
            else:
                message = f"Incorrecto. La respuesta correcta era: {correct_option.text}"
        except Question.DoesNotExist:
            return HttpResponseNotFound("La pregunta no existe.")
        except correct_option.DoesNotExist:
            return HttpResponseNotFound("La opción correcta para esta pregunta no existe.")
        
        return render(request, 'trivia/answer.html', {'message': message})
    
    # Obtener la pregunta actual
    current_question_id = request.session.get('current_question_id')
    if current_question_id:
        try:
            current_question = Question.objects.get(id=current_question_id)
        except Question.DoesNotExist:
            return HttpResponseNotFound("La pregunta no existe.")
    else:
        # Si no hay current_question_id en la sesión, obtener la primera pregunta
        current_question = Question.objects.first()
        if current_question:
            request.session['current_question_id'] = current_question.id
    
    # Obtener las opciones relacionadas con la pregunta actual
    options = current_question.option_set.all()

    return render(request, 'trivia/trivia_game.html', {'question': current_question, 'options': options})

def restart_game(request):
    # Eliminar el current_question_id de la sesión para reiniciar el juego
    if 'current_question_id' in request.session:
        del request.session['current_question_id']
    return redirect('trivia:trivia')
