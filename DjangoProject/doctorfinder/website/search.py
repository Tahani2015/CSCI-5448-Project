
from .models import Doctor

class Search():
    def __init__(self, state, city, zip, specialty):
        self.state = state
        self.city = city
        self.zip = zip
        self.specialty = specialty

    def doSearch(self):
        self.results = Doctor.objects.filter(speciality=self.specialty, state=self.state, city=self.city, zip=self.zip)     
        self.sortType.sort(self.results)

    def setSort(self, sortType):
        self.sortType = sortType
