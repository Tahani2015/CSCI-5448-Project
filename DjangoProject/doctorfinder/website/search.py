
from .models import Doctor, Insurance

class Search():
    def __init__(self, specialty, city, state, zip, insurance):
        self.specialty = specialty
        self.city = city
        self.state = state
        self.zip = zip
        self.insurance=insurance

    def doSearch(self):
        docResults = Doctor.objects.filter(speciality=self.specialty, city=self.city, state=self.state, zip=self.zip)
        #print('docObjects: ',docResults)     
        insResults = Insurance.objects.filter(name=self.insurance)
        #print('insObjects: ',insResults)
        docList=[doc.username.username for doc in docResults]
        #print('doclist: ',docList)
        insList=[doc.doctor.username.username for doc in insResults]
        #print('inslist: ',insList)
        inters_list= list(set(docList).intersection(insList))
        #print('intersection: ',inters_list)
        doctors=[]
        for doc in inters_list: 
            doctors.append(Doctor.objects.get(username=doc))
               
        self.results=doctors
        self.sortType.sort(self.results)

    def setSort(self, sortType):
        self.sortType = sortType
