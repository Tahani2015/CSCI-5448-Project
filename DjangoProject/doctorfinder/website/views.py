from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.template.context_processors import csrf

from .forms import SearchForm
from .search import Search
from website.models import Doctor

def index(request):
	# return HttpResponse('<p> In index view</p>')
	#doctors=Doctor.objects.exclude(username='Sara_George@gmail.com')
   	#return render(request, 'website/index.html', {
   	#	'doctors':doctors,
   	#	})
    context = {}
    context.update(csrf(request))
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #do search with classes?
            search = Search(form.cleaned_data['state'],
                            form.cleaned_data['city'],
                            form.cleaned_data['zip'],
                            form.cleaned_data['specialty'],)
            #actually do search
            results=search.doSearch()
            #store search objects into our session information for use
            #in search view
            request.session['search'] = search
            request.session['results'] = results
            return HttpResponseRedirect('search.html')
    else:
        form = SearchForm();

    context['form'] = form
    return render(request, 'website/index.html', context)

def search(request):
    context = {}
    context.update(csrf(request))
    context['search'] = request.session['search']
    context['results'] = request.session['results']
    return render(request, 'website/search.html', context);
   
