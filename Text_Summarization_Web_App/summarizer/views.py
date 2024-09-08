from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
import pickle
from .SummarizationPipeline import SummarizationPipeline




def summarize_text(request):
    summarized_text = ''
    if request.method == 'POST':
        summarizer = SummarizationPipeline()
        input_text = request.POST.get('text', '')
        summarized_text = summarizer.generate_summary(text=input_text)
        return render(request, 'summarizer/summarize_form.html', {'summary': summarized_text})
    else:
        return render(request, 'summarizer/summarize_form.html')