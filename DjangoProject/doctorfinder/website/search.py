from .models import Doctor

class Search():
    def __init__(self, state, city, zip, specialty):
        self.state = state
        self.city = city
        self.zip = zip
        self.specialty = specialty

    def doSearch(self):
        return Doctor.objects.filter(speciality=self.specialty)

    def setSort(sort):
        self.sort = sort

    def __viewSearchResults(results):
        pass
