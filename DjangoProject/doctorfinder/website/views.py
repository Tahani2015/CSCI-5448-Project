from django.shortcuts import render, redirect
from django.http import Http404

from .forms import SearchForm, SignUpForm
from .search import Search
from .sort import RatingSort, AvailabilitySort
from .models import User

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = Search(form.cleaned_data['specialty'],
                            form.cleaned_data['city'],
                            form.cleaned_data['state'],
                            form.cleaned_data['zip'],
                            form.cleaned_data['insurance'],)
            
            search.setSort(RatingSort())
            search.doSearch()
        #store search objects into our session information for use in search results
            request.session['search'] = search         
            return redirect('search_results.html')
    else:
        form = SearchForm();

    return render(request, 'website/index.html', {'form': form})

def search_results(request):
    doctors= request.session['search']
    return render(request, 'website/search_results.html', {'doctors':doctors})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.type = User.USER_CHOICES[1][1]
            new.save()
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'website/signup.html', {'form': form})
   
