from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.template.context_processors import csrf

from .forms import SearchForm
from website.models import Doctor

def index(request):
	# return HttpResponse('<p> In index view</p>')
	#doctors=Doctor.objects.exclude(username='Sara_George@gmail.com')
   	#return render(request, 'website/index.html', {
   	#	'doctors':doctors,
   	#	})
    context = {};
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #do search with classes?
            return HttpResponseRedirect('')
    else:
        form = SearchForm();

    context.update(csrf(request))
    context['form'] = form
    return render(request, 'website/index.html', context)
   
