from django.shortcuts import render, HttpResponse
from .models import TextResult
from .ai_cal import run_assistant

def placeholder_func(inp):
    return f"you said '{inp}'"
def process_text(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')
        # Call your Python function to process the text here
        processed_text = run_assistant(input_text)
        #result = TextResult(input_text=input_text, processed_text=processed_text)
        #result.save()  # Save the result to the database if desired
        return render(request, 'results.html', {'processed_text': processed_text})
    else:
        return render(request, 'index.html')