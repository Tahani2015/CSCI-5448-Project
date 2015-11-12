from django.shortcuts import render, redirect, get_object_or_404

from .forms import SearchForm
from .search import Search
from .sort import RatingSort, AvailabilitySort
from .models import Doctor, Review, Insurance

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = Search(form.cleaned_data['speciality'],
                            form.cleaned_data['city'],
                            form.cleaned_data['state'],
                            form.cleaned_data['zip'],
                            form.cleaned_data['insurance'],)
            
            search.setSort(RatingSort())
            search.doSearch()
            if search.results== [] : print "No results! " # Alert msg
            else:
                #store search objects into our session information for use in search results
                request.session['search'] = search
                return redirect('search_results.html')
    else:
        form = SearchForm()
    return render(request, 'website/index.html', {'form': form})

def search_results(request):
    doctors= request.session['search']
    return render(request, 'website/search_results.html', {'doctors':doctors})
   
def doctor_detail(request, pk):
    doctor=get_object_or_404(Doctor, username=pk)
    insurances=Insurance.objects.filter(doctor=pk)
    reviews=Review.objects.filter(doctor=pk)
    return render(request, 'website/doctor_detail.html', {'doctor': doctor, 'insurances': insurances, 'reviews': reviews})
   