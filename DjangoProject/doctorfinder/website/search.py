
from .models import Doctor

from .sort import RatingSort, AvailabilitySort


class Search():
    def __init__(self, state, city, zip, specialty):
        self.state = state
        self.city = city
        self.zip = zip
        self.specialty = specialty

    def doSearch(self):
        #do search, either with databaseproxy or django builtin
        return Doctor.objects.filter(speciality=self.specialty)
        #build objects
        results = __viewSearchResults(results)
        #sort
        results = self.sort.sort(results)
        self.results = results

    def setSort(sort):
        self.sort = sort

    def __viewSearchResults(results):
        pass
