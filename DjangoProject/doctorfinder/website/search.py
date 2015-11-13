
from .models import Doctor, Insurance

class Search():
    def __init__(self, speciality, city, state, zip, insurance):
        self.speciality = speciality
        self.city = city
        self.state = state
        self.zip = zip
        self.insurance=insurance

    def doSearch(self):
        docResults = Doctor.objects.filter(speciality=self.speciality, city=self.city, state=self.state, zip=self.zip)
        #print('docObjects: ',docResults[0].values())     
        insResults = Insurance.objects.filter(name=self.insurance)
        #print('insObjects: ',insResults.values())
        docList=[doc.username_id for doc in docResults]
        #print('doclist: ',docList)
        insList=[doc.doctor_id for doc in insResults]
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
