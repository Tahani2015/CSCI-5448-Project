
from .models import Doctor


class Search():
    def __init__(self, state, city, zip, specialty):
        self.state = state
        self.city = city
        self.zip = zip
        self.specialty = specialty

    def doSearch(self):
        #sort
        results = self.sort.sort(Doctor.objects.filter(speciality=self.specialty, state=self.state, city=self.city, zip=self.zip))
        self.results = results
        return self.results

    def setSort(self, sort):
        self.sort = sort
