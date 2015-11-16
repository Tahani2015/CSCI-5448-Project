from __future__ import division
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .forms import *
from .search import Search
from .sort import RatingSort, AvailabilitySort
from .login import LoginType
from .models import Doctor, Review, Insurance, User, FavoriteDoctors

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
            review.patient_id = request.session['user']  # The user currently logged in 
            review.save()
        # update doctor's rating    
            newRating=calculate_rating(pk)
            doctor=Doctor.objects.get(username=pk)
            doctor.rating=newRating
            doctor.save()
            return redirect('website.views.doctor_detail', pk=pk)
    else:
        form = ReviewForm();
    return render(request, 'website/review_add.html', {'form': form})

def calculate_rating(pk):
    reviews=Review.objects.filter(doctor=pk)
    ratingSum=0
    for review in reviews:
        ratingSum+=review.rating
    newRating=ratingSum/len(reviews)
    return newRating

def add_favorite(request, pk):
    favorite=FavoriteDoctors(patient_id=request.session['user'], doctor_id=pk)
    favorite.save()
    return redirect('website.views.doctor_detail', pk=pk)

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
            request.session['user'] = form.cleaned_data['username']
            userPage=LoginType(request.session['user']).redirectUser()
            return userPage
    else:
        form = LoginForm();
    return render(request, 'website/login.html', {'form': form})
   
def my_profile(request):
    user=User.objects.get(username=request.session['user'])
    if user.type == 'Patient':
        patient=User.objects.get(username=request.session['user'])
        favourites=FavoriteDoctors.objects.filter(patient_id=request.session['user'])
        docList=[favourite.doctor_id for favourite in favourites]
        doctors=[]
        for doc in docList: 
            doctors.append(Doctor.objects.get(username=doc))
        return render(request, 'website/patient_profile.html', {'patient' : patient, 'doctors': doctors})
    else:
        return render(request, 'website/doctor_profile.html', {})

def remove_favdoc(request, pk):
    favourite_doc=FavoriteDoctors.objects.get(doctor_id=pk, patient_id=request.session['user'])
    favourite_doc.delete()
    return redirect('website.views.my_profile')

def edit_patprofile(request):
    if request.method == 'POST':
        form = EditPatProForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.type = User.USER_CHOICES[1][1]
            new.save()
            return redirect('website.views.my_profile')
    else:
        form = EditPatProForm()
    return render(request, 'website/edit_patient_profile.html', {'form': form})

def edit_docprofile(request, pk):
    doctor = Doctor.objects.get(username=pk)
    if request.method == 'POST':
        form = EditDocProForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('website.views.doctor_detail', pk=pk)
    else:
        #make model data appear in form by default
        form = EditDocProForm(instance=doctor)
    return render(request, 'website/edit_doctor_profile.html', {'form': form})
    
