from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .forms import SearchForm, SignUpForm, ReviewForm, LoginForm, SetSortForm
from .search import Search
from .sort import RatingSort, AvailabilitySort
from .models import Doctor, Review, Insurance, User

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
                return redirect('website.views.search_results')
    else:
        form = SearchForm()
    return render(request, 'website/index.html', {'form': form})

def search_results(request):
    doctors= request.session['search']
    if request.method == 'POST':
        form = SetSortForm(request.POST)
        if form.is_valid():
            sort_type = form.cleaned_data['choice_field']
            doctors.reSort(sort_type)
    else:
        form = SetSortForm()
    return render(request, 'website/search_results.html', {'doctors':doctors, 'form':form})
   
def doctor_detail(request, pk):
    doctor=get_object_or_404(Doctor, username=pk)
    insurances=Insurance.objects.filter(doctor=pk)
    reviews=Review.objects.filter(doctor=pk)
    return render(request, 'website/doctor_detail.html', {'doctor': doctor, 'insurances': insurances, 'reviews': reviews})

def add_review(request, pk):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor_id = pk
            review.patient_id = request.session['user']   # The user currently logged in 
            review.save()
            return redirect('website.views.doctor_detail', pk=pk)
    else:
        form = ReviewForm();
    return render(request, 'website/review_add.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.type = User.USER_CHOICES[1][1]
            new.save()
            return redirect('website.views.login')
    else:
        form = SignUpForm()
    return render(request, 'website/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user=User.objects.get(username=form.cleaned_data['username'])
            if user.type == 'Patient':
                return redirect('/')
            elif user.type == 'Doctor':
                return redirect('website.views.doctor_detail', pk=user.username) 
            else:
                return redirect('/admin')
            request.session['user'] = user.username     
    else:
        form = LoginForm();
    return render(request, 'website/login.html', {'form': form})
   